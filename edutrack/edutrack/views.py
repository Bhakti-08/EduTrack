from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages
import csv,io
from main.models import TestAttempt, Subjects, Branch, TestDetails, Professors, Students, QuestionBank, Questions, StudentScores,StudentResponses
from datetime import datetime
from datetime import date
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
import random
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction
#from django.core.paginator import Paginator
#from django.db import IntegrityError, transaction
#from django.db import models
#from . import models
#from django.contrib.auth.decorators import permission_required

def index(request):
    if request.method=='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            #print(request.user.is_authenticated)
            if role=='Professor':
                    request.session['username'] = username
                    request.session['role'] = role
                    subject = Subjects.objects.get(subjectID=username)
                    request.session['branch'] = subject.branch.branch
                    return redirect('profHome')
            
            if role=='Student':
                    request.session['username'] = username
                    request.session['role'] = role
                    student = Students.objects.get(registrationNum=request.session['username'])
                    request.session['branch'] = student.branch
                    return redirect('studentHome')

        else:
            return HttpResponse('Enter valid login details...')
    else:
        if request.user.is_authenticated:
            if 'role' in request.session and request.session['role'] == 'Student':
                return redirect('studentHome')
            elif 'role' in request.session and request.session['role'] == 'Professor':
                return redirect('profHome')
            else:
                return redirect('logout')
        return render(request, 'index.html',{'data':''})

@csrf_protect
@login_required(login_url='login/')
def profHome(request):
    username = request.session['username']
    professor = Professors.objects.get(subjectID=username)
    name = professor.firstName + " " + professor.lastName
    subjectID = professor.subjectID
    branch = professor.branch
    email = professor.email
    output = {'data':username,'name':name ,'subjectID':subjectID,'branch':branch ,'email':email}
    return render(request,'profHome.html',output)

@csrf_protect
@login_required(login_url='login/')
def studentHome(request):
    username = request.session['username']
    student = Students.objects.get(registrationNum=request.session['username'])
    name = student.firstName + " " + student.lastName
    registrationNum = student.registrationNum
    branch = student.branch
    email = student.email
    output = {'data':username,'name' :name ,'registrationNum' : registrationNum,'branch' : branch,'email' : email}
    return render(request,'studentHome.html',output)

#return render(request,'studentHome.html',{'data':username})


def profRegistrationForm(request):
    if request.method=='POST':
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        branch = request.POST.get('branch')
        subjectID = request.POST.get('subjectID')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if(password==pass2):
            new_user = Professors(firstName=firstName,lastName=lastName,branch=branch,subjectID=subjectID,email=email,password=password)
            new_user.save()
            my_user = User.objects.create_user(subjectID,email,password)
            my_user.save()
            return redirect('login')
        else:
            data = '</br><b>Provide valid details!!</b>'
            return render(request, 'profRegistrationForm.html',{'data':data})
    else:
        return render(request, 'profRegistrationForm.html',{'data':''})

def studentRegistrationForm(request):
    if request.method=='POST':
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        branch = request.POST.get('branch')
        registrationNum = request.POST.get('registrationNum')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if(password==pass2):
            new_user = Students(firstName=firstName,lastName=lastName,branch=branch,registrationNum=registrationNum,email=email,password=password)
            new_user.save()
            my_user = User.objects.create_user(registrationNum,email,password)
            my_user.save()
            return redirect('login')
        else:
            data = '</br><b>Provide valid details!!</b>'
            return render(request, 'studentRegistrationForm.html',{'data':data})
    else:
        return render(request, 'studentRegistrationForm.html',{'data':''})


@csrf_protect
def logoutPage(request):
    if 'role' in request.session:
        del request.session['role']
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('login')

@csrf_protect
#@login_required(login_url='login')
def upload_questionBank(request):
    subID = request.session['username']
    # defining order of content in csv file
    try:
        prompt = {
            'order': '<b>NOTE:</b> Order of CSV file contents should be question, option_1, option_2, option_3, option_4, correct_option'
        }
        # checking whether the method is POST or not
        if request.method == 'GET':
            return render(request,'upload_questionBank.html',prompt)
        csv_file = request.FILES['file']    # 'file' is name given to that uploaded file in test-arranged.html 
        data = ''
        # checking whether uploaded file is CSV or not
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Uploaded file is not CSV File !!!')
            return render(request, 'upload_questionBank.html', {'data':data})
        #temp = Professors.objects.get(subjectID=subID)
        #subID = temp.subjectID
        obj = QuestionBank(subjectID=subID,questionBank=csv_file)
        obj.save()
        data = '</br><b>Your File Is Sucessfully Uploaded :)</b>'
        return render(request, 'upload_questionBank.html', {'data':data})
    except:
        return render(request,'profHome.html',{'data':obj.subID})
    
@csrf_protect
@transaction.atomic
def addingTest(request):
    subID = request.session['username']
    if request.method=='POST':
        try:
            with transaction.atomic():
                obj1 = Professors.objects.get(subjectID=subID)
                branch = Branch.objects.get(branch=obj1.branch)
                #branchID = branch.id
                subject = Subjects.objects.get(subjectID=subID)
                #subjectID = subject.id
                testName = request.POST.get('testName')
                numberOfQuestions = int(request.POST.get('numberOfQuestions'))
                testDate = request.POST.get('testDate')
                testStartTime = request.POST.get('testStartTime')
                testEndTime = request.POST.get('testEndTime')
                new_test = TestDetails(branch=branch,subject=subject,testName=testName,numberOfQuestions=numberOfQuestions,DateOfExam=testDate,StartTime=testStartTime,EndTime=testEndTime)
                new_test.save()
                obj2 = QuestionBank.objects.get(subjectID=subID)
                p = 'G:/EduTrack/edutrack/media/'+str(obj2.questionBank)
                file = open(p)
                csvFile = csv.reader(file)
                
                lines =[]
                for i in csvFile:
                    lines.append(i)
                l = len(lines)
                for i in range(0,numberOfQuestions):
                    j = random.randrange(0,l-1)
                    records = lines[j]
                    new_question = Questions(test = new_test,question = records[0],opt_1 = records[1],opt_2 = records[2],opt_3 = records[3],opt_4 = records[4],right_opt = records[5])
                    new_question.save()
                username = request.session['username']
            return redirect('profHome')
        except Exception:
            return HttpResponse('Failed to arrange test :(')
    return render(request,'addingTest.html')

def test_question(request, test_id):
    test = TestDetails.objects.get(id=test_id)
    questions = Questions.objects.filter(test=test).order_by('id')
    date = test.DateOfExam
    start_time = test.StartTime
    end_time = test.EndTime
    startDatetime = datetime.combine(date, start_time)
    endDatetime = datetime.combine(date, end_time)
    duration = int((endDatetime - startDatetime).total_seconds())
    student = Students.objects.get(registrationNum=request.session['username'])
    attempt, created = TestAttempt.objects.get_or_create(student=student, test=test, startTime=test.StartTime, endTime=test.EndTime)
    student_responses = StudentResponses.objects.filter(attempt=attempt)
    responses = dict()
    for res in student_responses:
        responses[res.question.id] = res.selectedAnswer

        # Get or create the StudentScores object
    obj, created = StudentScores.objects.get_or_create(Student=student, test=test)

    if created:
        # Initialize timeRemaining to the total duration of the test
        timeRemaining = duration
    else:
        # Retrieve the timeRemaining value if the object already exists
        timeRemaining = obj.TimeRemaining

    output = {'final_questions': questions, 'subject': test, 'timeRemaining':timeRemaining, 'attempt': attempt, 'responses': responses, 'start_time': startDatetime, 'end_time':endDatetime}
    return render(request, 'test-question.html', output)

def testSubmitted(request,test_id):
    if request.method=='POST':
        test = TestDetails.objects.get(id=test_id)
        student = Students.objects.get(registrationNum=request.session['username'])
        attempt = TestAttempt.objects.get(test=test, student=student)
        questions = Questions.objects.filter(test=test).order_by('id')
        studentResponses = StudentResponses.objects.filter(attempt=attempt)
        score=0
        wrong=0
        correct=0
        for q in questions:
            try:
                response = studentResponses.get(question=q)
                if q.right_opt == response.selectedAnswer:
                    score += 1
                    correct += 1
                else:
                    wrong += 1
            except StudentResponses.DoesNotExist:
                # Handle case where the student did not answer the question
                pass
        attempt.isSubmitted = True
        attempt.save()
        studentScore = StudentScores.objects.update_or_create(test=test,Student=student)[0]
        studentScore.correctAns = correct
        studentScore.wrongAns = wrong
        studentScore.score = score
        studentScore.save()
        #studentScore = StudentScores.objects.update(test=test, Student=student,correctAns=correct,wrongAns=wrong,score=score)
        return render(request, 'testSubmitted.html')
    return render(request, 'testSubmitted.html')

@login_required(login_url='/')
def studentResults(request):
    # Retrieve all TestAttempt objects associated with the current student
    Student = Students.objects.get(registrationNum=request.session['username'])
    test_attempts = TestAttempt.objects.filter(student=Student)
    name =  Student.firstName +' '+ Student.lastName

    # Create a list of dictionaries containing test details and scores for each attempt
    results = []
    for attempt in test_attempts:
        scores = StudentScores.objects.get(test=attempt.test, Student=Student)
        result = {
            'test_name': attempt.test.testName,
            'subject': attempt.test.subject,
            'date': attempt.test.DateOfExam,
            'score': scores.score,
            'correct_ans': scores.correctAns,
            'wrong_ans': scores.wrongAns
        }
        results.append(result)


    # Pass the results to the template for display
    context = {'results': results, 'name':name}
    return render(request, 'studentResults.html', context)

@login_required(login_url='/')
def testsForResults(request ):
    subID = request.session['username']
    subject = Subjects.objects.get(subjectID=subID)
    tests = TestDetails.objects.filter(subject=subject)
    submitted_tests = []
    for test in tests:
        if test.DateOfExam < timezone.now().date(): # check if the current date is not greater than DateOfExam for this test
            submitted_tests.append(test)
    return render(request, 'testsForResults.html', {'data':submitted_tests})



@login_required(login_url='/')
def testResults(request, test_id):
    # Retrieve the current test and associated scores
    test = TestDetails.objects.get(id=test_id)
    scores = StudentScores.objects.filter(test=test)

    # Create a list of dictionaries containing student details and scores for each attempt
    results = []
    for score in scores:
        student = score.Student
        result = {
            'registration_num': student.registrationNum,
            'name': student.firstName + ' ' + student.lastName,
            'branch': student.branch,
            'score': score.score,
            'correct_ans': score.correctAns,
            'wrong_ans': score.wrongAns
        }
        results.append(result)

    # Pass the results to the template for display
    context = {'test': test, 'results': results}
    return render(request, 'testResults.html', context)

@csrf_protect
def selectTest(request):
    branch = Branch.objects.get(branch=request.session['branch'])
    subjects = Subjects.objects.filter(branch=branch).order_by('id')
    tests = TestDetails.objects.filter(subject__in=subjects).order_by('id')
    current_date = timezone.now().date() # get the current date in the timezone of your Django project
    active_tests = []
    resume_tests = []
    submitted_tests = [] # create an empty list to store the tests that can be given
    upcoming_tests = []
    deactive_tests = []
    if(request.session['role']=='Student'):
        student = Students.objects.get(registrationNum=request.session['username'])
        for test in tests:
            if TestAttempt.objects.filter(test=test,student=student).exists():
                attempt = TestAttempt.objects.get(test=test, student=student)
                if(test.DateOfExam >= current_date ) :
                    if(attempt.isSubmitted != True) :
                 # check if the current date is not greater than DateOfExam for this test
                        resume_tests.append(test)
                    else :
                        submitted_tests.append(test)
            elif(test.DateOfExam >= current_date):
                active_tests.append(test)
            else :
                pass
    else:
        for test in tests:
            if(test.DateOfExam >= current_date ) :
                upcoming_tests.append(test)
            else :
                deactive_tests.append(test)
    output = {'active_tests':active_tests,'resume_tests':resume_tests,'submitted_tests':submitted_tests,'upcoming_tests':upcoming_tests,'deactive_tests':deactive_tests}
    return render(request, 'selectTest.html',output)

@csrf_protect
def updateStudentProfile(request):
    student =Students.objects.get(registrationNum=request.session['username'])
    if request.method=='POST':
        firstName = request.POST.get('fname').strip()
        lastName = request.POST.get('lname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password1').strip()
        pass2 = request.POST.get('password2').strip()
        data = ""
        if password==pass2 and firstName is not None and lastName is not None and email is not None:
            user = User.objects.get(username = request.session['username'])
            if user:
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                student.firstName = firstName
                student.lastName = lastName
                student.email = email

                if password is not None:
                    user.set_password(password)                    
                    student.password = password
                user.save()
                student.save()
        else:
            data = '</br><b>Provide valid details!!</b>'
            return render(request, 'updateStudentProfile.html',{'data':data,'student':student})
    else:
        return render(request, 'updateStudentProfile.html',{'data':'','student':student})


@csrf_protect
def updateProfessorProfile(request):
    professor = Professors.objects.get(subjectID=request.session['username'])
    if request.method=='POST':
        firstName = request.POST.get('fname').strip()
        lastName = request.POST.get('lname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password1').strip()
        pass2 = request.POST.get('password2').strip()
        data = ""
        if password==pass2 and firstName is not None and lastName is not None and email is not None:
            user = User.objects.get(username = request.session['username'])
            if user:
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                professor.firstName = firstName
                professor.lastName = lastName
                professor.email = email

                if password is not None:
                    user.set_password(password)                    
                    professor.password = password
                user.save()
                professor.save()
        else:
            data = '</br><b>Provide valid details!!</b>'
        return render(request, 'updateProfessorProfile.html',{'data':data, 'professor': professor})
    else:
        return render(request, 'updateProfessorProfile.html',{'data':'', 'professor': professor})
    
'''@login_required(login_url='login')
@csrf_protect
def selectTest(request) :
    branch = Branch.objects.get(branch=request.session['branch'])
    subjects = Subjects.objects.filter(branch=branch).order_by('id')
    tests = TestDetails.objects.filter(subject__in=subjects).order_by('id')
    student = Students.objects.get(registrationNum=request.session['username'])
    current_date = timezone.now().date() # get the current date in the timezone of your Django project
    obj = [] # create an empty list to store the tests that can be given
    for test in tests:
        if TestAttempt.objects.filter(test=test,student=student).exists():
            attempt = TestAttempt.objects.get(test=test, student=student)
            if(test.DateOfExam >= current_date and attempt.isSubmitted != True ) :
                obj.append(test)# check if the current date is not greater than DateOfExam for this test
        elif(test.DateOfExam >= current_date): # check if the current date is not greater than DateOfExam for this test
            obj.append(test)
        else : 
            pass
    return render(request, 'selectTest.html', {'data': obj})

def studentProfile(request):
    student = Students.objects.get(registrationNum=request.session['username'])
    name = student.firstName + " " + student.lastName
    registrationNum = student.registrationNum
    branch = student.branch
    email = student.email
    output = {'name' :name ,'registrationNum' : registrationNum,'branch' : branch,'email' : email}
    return render(request,'studentProfile.html',output)'''

