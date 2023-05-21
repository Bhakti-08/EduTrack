from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages
import csv,io
from main.models import TestAttempt, Branch, TestDetails, Professors, Students, QuestionBank, Questions, StudentScores,StudentResponses,HODs,SubjectToProfessor
from datetime import datetime,date
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
import random
from django.contrib.sessions.backends.db import SessionStore
from django.db import transaction

# Login Page

def index(request):
    if request.method=='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            if role=='Student':
                if Students.objects.filter(registrationNum=username).exists():
                    login(request,user)
                    request.session['username'] = username
                    request.session['role'] = role
                    student = Students.objects.get(registrationNum=username)
                    request.session['branch'] = student.branch
                    return redirect('studentHome')
                else:
                    messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')
                

            if role=='Professor':
                if Professors.objects.filter(email=username).exists():
                    login(request,user)
                    request.session['username'] = username
                    request.session['role'] = role
                    professor =Professors.objects.get(email=username)
                    request.session['branch'] = professor.branch
                    return redirect('profHome')
                else:
                    messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')
                    return render(request, 'index.html',{'data':''})

            if role=='HOD':
                if HODs.objects.filter(email=username).exists():
                    login(request,user)
                    request.session['username'] = username
                    request.session['role'] = role
                    hod = HODs.objects.get(email=username)
                    request.session['branch'] = hod.branch
                    return redirect('hodHome')
                else:
                    messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')
                    return render(request, 'index.html',{'data':''})
            
        else:
            messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')
            return render(request, 'index.html',{'data':''})
    else:
        if request.user.is_authenticated:
            if 'role' in request.session and request.session['role'] == 'Student':
                return redirect('studentHome')
            elif 'role' in request.session and request.session['role'] == 'Professor':
                return redirect('profHome')
            elif 'role' in request.session and request.session['role'] == 'HOD':
                return redirect('hodHome')
            else:
                return redirect('logout')
        return render(request, 'index.html',{'data':''})

# Logout

@csrf_protect
def logoutPage(request):
    if 'role' in request.session:
        del request.session['role']
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect('login')

# Registration

def registration(request):
    if request.method == 'POST':

        # For Student Registration

        if 'student-registration' in request.POST:
            firstName = request.POST.get('fname')
            lastName = request.POST.get('lname')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            branch = request.POST.get('branch')
            registrationNum = request.POST.get('registrationNum')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if(password==pass2):
                special_characters = "!@#$%^&*()-+"
                if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                    messages.error(request, 'Please use strong password!', extra_tags='badpassword')  
                    branches = Branch.objects.all()
                    data = {'data': '', 'branches': branches }         
                    return render(request, 'registration.html',data)
                #if(len(password)>=8 and password.isalnum() ):
                else :
                    new_user = Students(firstName=firstName,lastName=lastName,gender=gender,college=college,branch=branch,registrationNum=registrationNum,email=email,password=password)
                    new_user.save()
                    my_user = User.objects.create_user(registrationNum,email,password)
                    my_user.first_name = firstName
                    my_user.last_name = lastName
                    my_user.save()
                    messages.success(request, 'You have registered successfully!', extra_tags='RegisterStud')
                    return redirect('login')
            else:
                branches = Branch.objects.all()
                data = {'branches': branches}
                messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterStud')           
                return render(request, 'registration.html',data)
        
        # For Professor Registration

        if 'professor-registration' in request.POST:
            firstName = request.POST.get('fname')
            lastName = request.POST.get('lname')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            branch = request.POST.get('department')
            #subjectID = request.POST.get('subjectID')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if(password==pass2):
                special_characters = "!@#$%^&*()-+"
                if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                    messages.error(request, 'Please use strong password!', extra_tags='badpassword')  
                    branches = Branch.objects.all()
                    data = {'data': '', 'branches': branches }         
                    return render(request, 'registration.html',data)
                else :
                    new_user = Professors(firstName=firstName,lastName=lastName,gender=gender,college=college,branch=branch,email=email,password=password)
                    new_user.save()
                    my_user = User.objects.create_user(email,email,password)
                    my_user.name = firstName
                    my_user.last_name = lastName
                    my_user.save()
                    messages.success(request, 'You have registered successfully!', extra_tags='RegisterProf')
                    return redirect('login')
            else:
                branches = Branch.objects.all()
                data = {'branches': branches}
                messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterProf')           
                return render(request, 'registration.html',data)
            
        # For HOD Registration

        if 'hod-registration' in request.POST:
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            branch = request.POST.get('branch')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if(password==pass2):
                special_characters = "!@#$%^&*()-+"
                if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                    messages.error(request, 'Please use strong password!', extra_tags='badpassword')  
                    branches = Branch.objects.all()
                    data = {'data': '', 'branches': branches }         
                    return render(request, 'registration.html',data)
                #if(len(password)>=8 and password.isalnum() ):
                else :
                    new_user = HODs(name=name,gender=gender,college=college,branch=branch,email=email,password=password)
                    new_user.save()
                    my_user = User.objects.create_user(username=email,email=email,password=password)              
                    my_user.save()
                    messages.success(request, 'You have registered successfully!', extra_tags='RegisterHOD')
                    return redirect('login')
            else:
                branches = Branch.objects.all()
                data = {'branches': branches}
                messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterHOD')           
                return render(request, 'registration.html',data)
    else:
        branches = Branch.objects.all()
        #subjects = Subjects.objects.all()
        data = {'data': '', 'branches': branches }
        return render(request, 'registration.html',data)

# Student Home Page

@csrf_protect
@login_required(login_url='login/')
def studentHome(request):
    student =Students.objects.get(registrationNum=request.session['username'])
    test_attempts = TestAttempt.objects.filter(student=student)
    name =  student.firstName +' '+ student.lastName

    # Create a list of dictionaries containing test details and scores for each attempt
    results = []
    for attempt in test_attempts:
        scores = StudentScores.objects.get(test=attempt.test, Student=student)
        result = {
            'test_name': attempt.test.testName,
            'subject': attempt.test.subjectID,
            'date': attempt.test.DateOfExam,
            'Total marks':scores.test.numberOfQuestions,
            'score': scores.score,
            'correct_ans': scores.correctAns,
            'wrong_ans': scores.wrongAns
        }
        results.append(result)

    if request.method == 'POST':

        # To Update Student Profile

        if 'update-student-profile-btn' in request.POST:
            firstName = request.POST.get('fname').strip()
            lastName = request.POST.get('lname').strip()
            email = request.POST.get('email').strip()
            password = request.POST.get('password1').strip()
            pass2 = request.POST.get('password2').strip()
            if password==pass2 and firstName is not None and lastName is not None and email is not None:
                user = User.objects.get(username = request.session['username'])
                if user:
                    user.first_name = firstName
                    user.last_name = lastName
                    user.email = email
                    student.firstName = firstName
                    student.lastName = lastName
                    student.email = email
                    if password:
                        user.set_password(password)                    
                        student.password = password
                    user.save()
                    student.save()
                    messages.success(request, 'Profile is updated successfully!', extra_tags='ProfileUpdated')
            else:
                messages.error(request, 'Invalid Details',extra_tags='InvalidDetails')
    return render(request,'studentHome.html',{'student':student , 'results': results, 'name':name})

# Professor Home Page

@csrf_protect
@login_required(login_url='login/')
def profHome(request):
    professor = Professors.objects.get(email=request.session['username'])
    subjects = SubjectToProfessor.objects.filter(profemail=request.session['username'] )
    branches = Branch.objects.all()
    questionbanks = []
    for subject in subjects:
        if QuestionBank.objects.filter(subjectID=subject.subjectID).exists():
            questionbank = {
                'subjectID' : subject.subjectID,
                'subjectName' : subject.subjectName,
                'exists' : True
            }
            questionbanks.append(questionbank)
        else :
            questionbank = {
                'subjectID' : subject.subjectID,
                'subjectName' : subject.subjectName,
                'exists' : False
            }
            questionbanks.append(questionbank)

    if request.method == 'POST':
        # check which submit button was clicked

        # To Upload Question Bank

        if 'upload-questionbank-btn' in request.POST:
            subID = request.POST.get('subjectID').strip()
            # defining order of content in csv file
            try:
                csv_file = request.FILES['file']    # 'file' is name given to that uploaded file in Uploading Questionbank session of profHome.html
                # checking whether uploaded file is CSV or not
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'Uploaded file is not CSV File !!!', extra_tags='NotCSVFile')
                else :
                    obj = QuestionBank(subjectID=subID,questionBank=csv_file)
                    obj.save()
                    messages.success(request, 'Questionbank is uploaded successfully!', extra_tags='SuccessInUpload')
            except:
                messages.error(request, 'Failed to upload question bank :(', extra_tags='FailedToUpload')

        if 'replace-questionbank-btn' in request.POST:
            subID = request.POST.get('subjectID')
            print(subID)
            if subID:
                subID = subID.strip()
                # rest of the code
            else:
                # handle the case when subjectID is not present or empty
                messages.error(request, 'Subject ID is missing or empty', extra_tags='SubjectIDMissing')
            # defining order of content in csv file
            try:
                csv_file = request.FILES['file']    # 'file' is name given to that uploaded file in Uploading Questionbank session of profHome.html
                # checking whether uploaded file is CSV or not
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'Uploaded file is not CSV File !!!', extra_tags='NotCSVFile')
                else :
                    obj = QuestionBank.objects.get(subjectID=subID)
                    obj.questionBank = csv_file
                    obj.save()
                    '''obj = QuestionBank(subjectID=subID,questionBank=csv_file)
                    obj.save()'''
                    messages.success(request, 'Questionbank is replaced successfully!', extra_tags='SuccessInReplace')
            except Exception as e:
                print(e)
                messages.error(request, 'Failed to replace question bank :(', extra_tags='FailedToReplace')

        # To Set Test

        elif 'set-test-btn' in request.POST:
            try:
                with transaction.atomic():
                    branch = request.session['branch']
                    subjectID = request.POST.get('subjectID')
                    testName = request.POST.get('testName')
                    numberOfQuestions = int(request.POST.get('numberOfQuestions'))
                    testDate = request.POST.get('testDate')
                    testStartTime = request.POST.get('testStartTime')
                    testEndTime = request.POST.get('testEndTime')
                    new_test = TestDetails(branch=branch,subjectID=subjectID,testName=testName,numberOfQuestions=numberOfQuestions,DateOfExam=testDate,StartTime=testStartTime,EndTime=testEndTime)
                    new_test.save()
                    obj2 = QuestionBank.objects.get(subjectID=subjectID)
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
                messages.success(request, 'Test is arranged successfully!', extra_tags='TestArranged')
    
            except Exception:
                messages.error(request, 'Failed to arrange test :(',extra_tags='TestArrangeFailed')
        
        # To Updatae Professor Profile

        elif 'update-professor-profile-btn' in request.POST:
            firstName = request.POST.get('fname').strip()
            lastName = request.POST.get('lname').strip()
            password = request.POST.get('password1').strip()
            pass2 = request.POST.get('password2').strip()
            if password==pass2 and firstName is not None and lastName is not None :
                user = User.objects.get(username = request.session['username'])
                if user:
                    user.first_name = firstName
                    user.last_name = lastName
                    professor.firstName = firstName
                    professor.lastName = lastName
                    if password:
                        user.set_password(password)                    
                        professor.password = password
                    user.save()
                    professor.save()
                    messages.success(request, 'Profile is updated successfully!', extra_tags='ProfileUpdated')
                    return redirect('profHome')
            else:
                messages.error(request, 'Invalid Details',extra_tags='InvalidDetails')

    return render(request,'profHome.html',{'professor': professor,'subjects' : subjects, 'branches': branches, 'questionbanks':questionbanks})

@csrf_protect
@login_required(login_url='login/')
def hodHome(request):
    hod = HODs.objects.get(email=request.session['username'])
    subjects = SubjectToProfessor.objects.filter(branch=hod.branch)
    professors = Professors.objects.all()

    if request.method == 'POST':

        # Assign new subject to Professor

        if 'add-subject-btn' in request.POST:
            branch = request.session['branch']
            subjectName  = request.POST.get('subjectName').strip()
            subjectID = request.POST.get('subjectID').strip()
            profemail = request.POST.get('profemail')
            if SubjectToProfessor.objects.filter(branch=branch,subjectName=subjectName,subjectID=subjectID).exists() :
                messages.error(request, 'Subject already exists !', extra_tags='AssignSubjectFailed')
            subject = SubjectToProfessor(branch=branch,subjectName=subjectName,subjectID=subjectID,profemail=profemail)
            subject.save()
            messages.success(request, 'Subject is assigned to professor successfully!', extra_tags='AssignedSubject')

        # Replace assigned subject to Professor

        if 'replace-professor-btn' in request.POST:
            branch = request.session['branch']
            subjectID = request.POST.get('subjectID').strip()
            profemail = request.POST.get('profemail').strip()
            subject = SubjectToProfessor.objects.get(branch=branch,subjectID=subjectID)
            subject.profemail = profemail
            subject.save()
            messages.success(request, 'Professor is replaced successfully!', extra_tags='ProfessorReplaced')

        # Delete subject

        if 'remove-subject-btn' in request.POST:
            branch = request.session['branch']
            subjectID = request.POST.get('subjectID').strip()
            subject = SubjectToProfessor.objects.get(branch = branch,subjectID=subjectID)
            subject.delete()
            messages.success(request, 'Subject is deleted successfully!', extra_tags='DeletedSubject')

        # To Update HOD Profile

        if 'update-hod-profile-btn' in request.POST:
            name = request.POST.get('name').strip()
            password = request.POST.get('password1').strip()
            pass2 = request.POST.get('password2').strip()
            if password==pass2 and name is not None :
                user = User.objects.get(username = request.session['username'])
                if user:
                    hod.name = name
                    if password:
                        user.set_password(password)                    
                        hod.password = password
                    user.save()
                    hod.save()
                    messages.success(request, 'Profile is updated successfully!', extra_tags='ProfileUpdated')
            else:
                messages.error(request, 'Invalid Details',extra_tags='InvalidDetails')
    return render(request,'hodHome.html',{'hod':hod,'subjects':subjects,'professors':professors })

# Tests

@csrf_protect
def selectTest(request):
    role = request.session['role']
    subjects = SubjectToProfessor.objects.filter(branch=request.session['branch']).order_by('id')
    tests = TestDetails.objects.filter(subjectID__in=subjects.values_list('subjectID', flat=True)).order_by('id')
    current_time = datetime.now()
    active_tests = []
    resume_tests = []
    upcoming_tests = []
    if(request.session['role']=='Student'):
        student = Students.objects.get(registrationNum=request.session['username'])
        for test in tests:
            date = test.DateOfExam
            start_time = test.StartTime
            end_time = test.EndTime
            startDatetime = datetime.combine(date, start_time)
            endDatetime = datetime.combine(date, end_time)
            # Add 30 minutes using timedelta
            new_enddatetime = endDatetime + timedelta(minutes=30)

            if TestAttempt.objects.filter(test=test,student=student).exists():
                attempt = TestAttempt.objects.get(test=test, student=student)
                if(startDatetime <= current_time and new_enddatetime >current_time and  attempt.isSubmitted != True) :
                 # check if the current date is not greater than DateOfExam for this test
                    resume_tests.append(test)
            elif(startDatetime <= current_time and endDatetime > current_time):
                active_tests.append(test)
            elif(startDatetime > current_time):
                upcoming_tests.append(test)
            else :
                pass
    else:
        for test in tests:
            date = test.DateOfExam
            start_time = test.StartTime
            end_time = test.EndTime
            startDatetime = datetime.combine(date, start_time)
            endDatetime = datetime.combine(date, end_time)
            if(startDatetime <= current_time and endDatetime > current_time) :
                active_tests.append(test)
            elif(startDatetime >= current_time) :
                upcoming_tests.append(test)
            else :
                pass
    output = {'role':role,'active_tests':active_tests,'resume_tests':resume_tests,'upcoming_tests':upcoming_tests,}
    return render(request, 'selectTest.html',output)

# Question Paper

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
                score = 0
                correct = 0
                wrong = 0
        attempt.isSubmitted = True
        attempt.save()
        studentScore = StudentScores.objects.update_or_create(test=test,Student=student)[0]
        studentScore.correctAns = correct
        studentScore.wrongAns = wrong
        studentScore.score = score
        studentScore.save()
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
        if(attempt.isSubmitted == True):
            scores = StudentScores.objects.get(test=attempt.test, Student=Student)
            subject = SubjectToProfessor.objects.get(subjectID=attempt.test.subjectID)
            result = {
                'test_name': attempt.test.testName,
                'subject': subject.subjectName,
                'date': attempt.test.DateOfExam,
                'Total_marks':scores.test.numberOfQuestions,
                'Scored_marks': scores.score,
            }
            results.append(result)
    # Pass the results to the template for display
    context = {'results': results, 'name':name}
    return render(request, 'studentResults.html', context)


@login_required(login_url='/')
def testsForResults(request ):
    subjects = SubjectToProfessor.objects.filter(profemail = request.session['username'])
    submitted_tests = []
    for subject in subjects :
        tests = TestDetails.objects.filter(subjectID=subject.subjectID)
        for test in tests:
            date = test.DateOfExam
            end_time = test.EndTime
            endDatetime = datetime.combine(date, end_time)
            # Add 30 minutes using timedelta
            new_enddatetime = endDatetime + timedelta(minutes=30)
            if new_enddatetime < datetime.now(): # check if the current time is not greater than enddatetime  for this test
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
            'Total_marks':score.test.numberOfQuestions,
            'Scored_Marks': score.score,
        }
        results.append(result)
    # Pass the results to the template for display
    context = {'test': test, 'results': results}
    return render(request, 'testResults.html', context)