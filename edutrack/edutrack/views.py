#from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import csv,io
import random
from main.models import College, Directors, HODs, Professors, Students, BranchToHOD, Branch, TestDetails, QuestionBank, Questions, StudentScores,StudentResponses,SubjectToProfessor
from datetime import datetime,date
#from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from edutrack.settings import BASE_DIR

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
                    request.session['branch'] = student.branch.branch
                    request.session['college'] = student.branch.college.name
                    return redirect('studentHome')
                else:
                    messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')

            if role=='Professor':
                if Professors.objects.filter(email=username).exists():
                    login(request,user)
                    request.session['username'] = username
                    request.session['role'] = role
                    professor =Professors.objects.get(email=username)
                    request.session['branch'] = professor.branch.branch
                    request.session['college'] = professor.branch.college.name
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
                    request.session['branch'] = hod.branch.branch
                    request.session['college'] = hod.branch.college.name
                    return redirect('hodHome')
                else:
                    messages.error(request, 'Enter valid login details...', extra_tags='FailedToLogin')
                    return render(request, 'index.html',{'data':''})
                
            if role=='Director':
                if College.objects.filter(directoremail=username).exists():
                    login(request,user)
                    request.session['username'] = username
                    request.session['role'] = role
                    director = Directors.objects.get(email=username)
                    request.session['college'] = director.college.name
                    return redirect('directorHome')
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
            elif 'role' in request.session and request.session['role'] == 'Director':
                return redirect('directorHome')
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
    if College.objects.exists() :
        colleges = College.objects.all()
        if Branch.objects.exists() :
            branches = Branch.objects.all()
        else:
            branches = ""
    else:
        colleges = ""       
        
    data = {'data':'' ,'colleges': colleges,'branches': branches }

    if request.method == 'POST':

        #For Director Registration
        if 'director-registration' in request.POST:
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Existing user..', extra_tags='UserExist')           
                return render(request, 'registration.html',data)
            elif College.objects.filter(name=college,directoremail=email).exists():
                if(password==pass2):
                    special_characters = "!@#$%^&*()-+"
                    if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                        messages.error(request, 'Please use strong password!', extra_tags='badpassword') 
                        return render(request, 'registration.html',data)
                    else:
                        College_obj = College.objects.get(name=college)
                        new_user = Directors(name=name,gender=gender,college=College_obj,email=email,password=password)
                        new_user.save()
                        my_user = User.objects.create_user(username=email,email=email,password=password)              
                        my_user.save()
                        messages.success(request, 'You have registered successfully!', extra_tags='RegisterDirector')
                        return redirect('login')
                else:
                    messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterDirector')           
                    return render(request, 'registration.html',data)
            else :
                messages.error(request, 'You are not assigned as a director', extra_tags='NotADirector')           
                return render(request, 'registration.html',data)
        
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
            college_obj = College.objects.get(name=college)
            college_email = college_obj.directoremail
            domain1 = college_email.split('@')[1]
            domain2 = email.split('@')[1]
            # Query the User model to check if any record has the provided username
            if User.objects.filter(username=registrationNum).exists():
                messages.error(request, 'Existing user..', extra_tags='UserExist')           
                return render(request, 'registration.html',data)
            else :
                if(domain1 == domain2) :
                    if(password==pass2):
                        special_characters = "!@#$%^&*()-+"
                        if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                            messages.error(request, 'Please use strong password!', extra_tags='badpassword')  
                            return render(request, 'registration.html',data)
                        else :
                            studbranch = Branch.objects.get(branch=branch,college__name=college)
                            new_user = Students(firstName=firstName,lastName=lastName,gender=gender,branch=studbranch,registrationNum=registrationNum,email=email,password=password)
                            new_user.save()
                            my_user = User.objects.create_user(registrationNum,email,password)
                            my_user.save()
                            messages.success(request, 'You have registered successfully!', extra_tags='RegisterStud')
                            return redirect('login')
                    else:
                        messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterStud')           
                        return render(request, 'registration.html',data)
                else :
                    messages.error(request, 'Provide college email Id ..', extra_tags='WrongEmailId')           
                    return render(request, 'registration.html',data)
        
        # For Professor Registration

        if 'professor-registration' in request.POST:
            firstName = request.POST.get('fname')
            lastName = request.POST.get('lname')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            branch = request.POST.get('branch')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            college_obj = College.objects.get(name=college)
            college_email = college_obj.directoremail
            domain1 = college_email.split('@')[1]
            domain2 = email.split('@')[1]
            # Query the User model to check if any record has the provided username
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Existing user..', extra_tags='UserExist')           
                return render(request, 'registration.html',data)
            else :
                if(domain1 == domain2) :
                    if(password==pass2):
                        special_characters = "!@#$%^&*()-+"
                        if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                            messages.error(request, 'Please use strong password!', extra_tags='badpassword')           
                            return render(request, 'registration.html',data)
                        else :
                            profbranch = Branch.objects.get(branch=branch,college__name=college)
                            new_user = Professors(firstName=firstName,lastName=lastName,gender=gender,branch=profbranch,email=email,password=password)
                            new_user.save()
                            my_user = User.objects.create_user(email,email,password)
                            my_user.first_name = firstName
                            my_user.last_name = lastName
                            my_user.save()
                            messages.success(request, 'You have registered successfully!', extra_tags='RegisterProf')
                            return redirect('login')
                    else:
                        messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterProf')           
                        return render(request, 'registration.html',data)
                else :
                    messages.error(request, 'Provide college email Id ..', extra_tags='WrongEmailId')           
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
            # Query the User model to check if any record has the provided username
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Existing user..', extra_tags='UserExist')           
                return render(request, 'registration.html',data)
            elif College.objects.filter(name=college).exists() :
                college_obj = College.objects.get(name=college)
                if Branch.objects.filter(branch=branch,college=college_obj).exists():
                    branch_obj = Branch.objects.get(branch=branch,college=college_obj)
                    if BranchToHOD.objects.filter(branch=branch_obj,hodemail=email).exists():
                        if(password==pass2):
                            special_characters = "!@#$%^&*()-+"
                            if (len(password) < 8) or (not any(char.isupper() for char in password)) or (not any(char.islower() for char in password)) or (not any(char.isdigit() for char in password)) or (not any(char in special_characters for char in password)):
                                messages.error(request, 'Please use strong password!', extra_tags='badpassword')       
                                return render(request, 'registration.html',data)
                            else :
                                hodbranch = Branch.objects.get(branch=branch,college__name=college)
                                new_user = HODs(name=name,gender=gender,branch=hodbranch,email=email,password=password)
                                new_user.save()
                                my_user = User.objects.create_user(username=email,email=email,password=password)              
                                my_user.save()
                                messages.success(request, 'You have registered successfully!', extra_tags='RegisterHOD')
                                return redirect('login')
                        else:
                            messages.error(request, 'Provide valid details...', extra_tags='FailedToRegisterHOD')           
                            return render(request, 'registration.html',data)
                    else :
                        messages.error(request, 'You are not assigned as a HOD for this department ..', extra_tags='NotAssignedHOD')           
                        return render(request, 'registration.html',data)
                else :
                    messages.error(request, 'Given department does not belong to given college..', extra_tags='BranchNotFound')           
                    return render(request, 'registration.html',data)
            else :
                messages.error(request, 'College not found ...', extra_tags='CollegeNotFound')           
                return render(request, 'registration.html',data)
    else:
        return render(request, 'registration.html',data)

# Director Home Page
@csrf_protect
@login_required(login_url='login/')
def directorHome(request):
    director = Directors.objects.get(email=request.session['username'])
    branches = BranchToHOD.objects.filter(branch__college = director.college)
    college_obj = College.objects.get(name=request.session['college'])
    college_email = college_obj.directoremail
    domain1 = college_email.split('@')[1]

    if request.method == 'POST':

        #To add new department with HOD
        if 'add-hod-btn' in request.POST:
            branchName = request.POST.get('branchName').strip()
            hodemail = request.POST.get('hodemail').strip()
            domain2 = hodemail.split('@')[1]
            if Branch.objects.filter(branch=branchName,college=director.college).exists():
                messages.error(request, "Can not add existing department ",extra_tags='AddHODFailed')
            else:
                if(domain1 == domain2) :
                    if BranchToHOD.objects.filter(hodemail=hodemail).exists():
                        messages.error(request, "Can not add existing hod for other department ",extra_tags='ExistingHOD')
                    else:
                        new_branch = Branch(branch=branchName,college=director.college)
                        new_branch.save()
                        new_hod = BranchToHOD(branch=new_branch, hodemail = hodemail)
                        new_hod.save()
                        messages.success(request, 'HOD is added successfully!', extra_tags='AddedHOD')
                else :
                    messages.error(request, 'Provide college email Id ..', extra_tags='WrongEmailId')           

        #To change HOD of existing department
        if 'change-hod-btn' in request.POST:
            branchName = request.POST.get('branchName').strip()
            hodemail = request.POST.get('hodemail').strip()
            branch = Branch.objects.get(branch=branchName,college=director.college)
            domain2 = hodemail.split('@')[1]
            if BranchToHOD.objects.filter(branch=branch,hodemail=hodemail).exists():
                messages.error(request, "Hod is already assigned to this department ",extra_tags='AlreadyAssighedHOD')
            else :
                if(domain1 == domain2) :
                    obj = BranchToHOD.objects.get(branch=branch)
                    obj.hodemail = hodemail
                    obj.save()
                    messages.success(request, 'HOD is changed successfully!', extra_tags='ChangedHOD')
                else :
                    messages.error(request, 'Provide college email Id ..', extra_tags='WrongEmailId') 

        #To Remove Department
        if 'remove-department-btn' in request.POST:
            branchName = request.POST.get('branchName').strip()
            branch = Branch.objects.get(branch=branchName,college=director.college)
            branch.delete()
            messages.success(request, 'Department is removed successfully!', extra_tags='DepartmentRemoved')

        #To change semister end date
        if 'change-semister-btn' in request.POST :
            sem1Date = request.POST.get('sem1date')
            sem2Date = request.POST.get('sem2date')
            college_obj = College.objects.get(directoremail=director.email)
            college_obj.semester1_End_date = sem1Date
            college_obj.semester2_End_date = sem2Date
            college_obj.save()
            messages.success(request, 'Semister duration changed successfully!', extra_tags='SemDurationChanged')


        # To Update director Profile
        if 'update-director-profile-btn' in request.POST:
            name = request.POST.get('name').strip()
            password = request.POST.get('password1').strip()
            pass2 = request.POST.get('password2').strip()
            if password==pass2 and name is not None :
                user = User.objects.get(username = request.session['username'])
                if user:
                    director.name = name
                    if password:
                        user.set_password(password)                    
                        director.password = password
                    user.save()
                    director.save()
                    messages.success(request, 'Profile is updated successfully!', extra_tags='ProfileUpdated')
            else:
                messages.error(request, 'Invalid Details',extra_tags='InvalidDetails')
    
    return render(request,'directorHome.html',{'director':director,'branches' :branches,'college_obj':college_obj})

# Student Home Page
@csrf_protect
@login_required(login_url='login/')
def studentHome(request):
    student = Students.objects.get(registrationNum=request.session['username'])

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
    return render(request,'studentHome.html',{'student':student })

# Professor Home Page
@csrf_protect
@login_required(login_url='login/')
def profHome(request):
    professor = Professors.objects.get(email=request.session['username'])
    subjects = SubjectToProfessor.objects.filter(profemail=request.session['username'] )
    branches = Branch.objects.filter(college=professor.branch.college)
    questionbanks = []
    for subject in subjects:
        if QuestionBank.objects.filter(college=professor.branch.college,subjectID=subject.subjectID).exists():
            questionbank = {
                'subjectID' : subject.subjectID,
                'subjectName' : subject.subjectName,
                'exists' : True
            }
        else :
            questionbank = {
                'subjectID' : subject.subjectID,
                'subjectName' : subject.subjectName,
                'exists' : False
            }
        questionbanks.append(questionbank)

    if request.method == 'POST':

        # To Upload Question Bank
        if 'upload-questionbank-btn' in request.POST:
            subID = request.POST.get('subjectID').strip()
            # defining order of content in csv file
            try:
                # 'file' is name given to that uploaded file in Uploading Questionbank session of profHome.html
                csv_file = request.FILES['file']
                # checking whether uploaded file is CSV or not
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'Uploaded file is not CSV File !!!', extra_tags='NotCSVFile')
                else :
                    obj = QuestionBank(college=professor.branch.college,subjectID=subID,questionBank=csv_file)
                    obj.save()
                    messages.success(request, 'Questionbank is uploaded successfully!', extra_tags='SuccessInUpload')
            except:
                messages.error(request, 'Failed to upload question bank :(', extra_tags='FailedToUpload')

        if 'replace-questionbank-btn' in request.POST:
            subID = request.POST.get('subjectID').strip()
            try:
                # 'file' is name given to that uploaded file in Uploading Questionbank session of profHome.html
                csv_file = request.FILES['file']
                # checking whether uploaded file is CSV or not
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'Uploaded file is not CSV File !!!', extra_tags='NotCSVFile')
                else :
                    obj = QuestionBank.objects.get(subjectID=subID,college=professor.branch.college)
                    obj.questionBank = csv_file
                    obj.save()
                    '''obj = QuestionBank(subjectID=subID,questionBank=csv_file)
                    obj.save()'''
                    messages.success(request, 'Questionbank is replaced successfully!', extra_tags='SuccessInReplace')
            except Exception :
                messages.error(request, 'Failed to replace question bank :(', extra_tags='FailedToReplace')
        
        # To Update Professor Profile
        elif 'update-professor-profile-btn' in request.POST:
            firstName = request.POST.get('fname').strip()
            lastName = request.POST.get('lname').strip()
            password = request.POST.get('password1').strip()
            pass2 = request.POST.get('password2').strip()
            if password==pass2 and firstName is not None and lastName is not None :
                user = User.objects.get(username = request.session['username'])
                if user:
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

#Tests Home Page for Professor
@csrf_protect
def testsHome(request):
    professor = Professors.objects.get(email=request.session['username'])
    branch = request.session['branch']
    college = request.session['college']
    college_obj = College.objects.get(name = college)
    branch_obj = Branch.objects.get(branch=branch,college=college_obj)
    subjects = SubjectToProfessor.objects.filter(branch=branch_obj,branch__college=college_obj)
    #subjects = SubjectToProfessor.objects.filter(branch__branch__branch=request.session['branch'],branch__branch__college__name=request.session['college']).order_by('id')
    prof_subjects = SubjectToProfessor.objects.filter(profemail=request.session['username'] )
    tests = TestDetails.objects.filter(subjectID__in=subjects.values_list('subjectID', flat=True)).order_by('id')
    current_time = datetime.now()
    active_tests = []
    upcoming_tests = []
    prof_upcoming_tests = []
    prof_tests = TestDetails.objects.filter(subjectID__in=prof_subjects.values_list('subjectID', flat=True)).order_by('id')
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

    for test in prof_tests :
        date = test.DateOfExam
        start_time = test.StartTime
        startDatetime = datetime.combine(date, start_time)
        if(startDatetime > current_time) :
            prof_upcoming_tests.append(test)          
                    
                    
    if 'set-test-btn' in request.POST:
        try:
            with transaction.atomic():
                subjectID = request.POST.get('subjectID')
                testName = request.POST.get('testName')
                numberOfQuestions = int(request.POST.get('numberOfQuestions'))
                testDate = request.POST.get('testDate')
                testStartTime = request.POST.get('testStartTime')
                testEndTime = request.POST.get('testEndTime')
                if TestDetails.objects.filter(branch=professor.branch,subjectID=subjectID,testName=testName).exists():
                    messages.error(request, 'Test name already exists ..',extra_tags='TestNameExists')
                else :
                    new_test = TestDetails(branch=professor.branch,subjectID=subjectID,testName=testName,numberOfQuestions=numberOfQuestions,DateOfExam=testDate,StartTime=testStartTime,EndTime=testEndTime)
                    new_test.save()                    
                    obj2 = QuestionBank.objects.get(college=professor.branch.college,subjectID=subjectID)
                    s = str(obj2.questionBank)
                    a = str(BASE_DIR)
                    p = a + '/media/'+s
                    file = open(p,encoding='utf8')           
                    csvFile = csv.reader(file)                  
                    lines =[]
                    for i in csvFile:
                        lines.append(i)                    
                    l = len(lines)
                    # Store the indices of selected rows
                    selected_rows= set()
                    for _ in range(numberOfQuestions):
                        while True:
                            j = random.randrange(0, l)
                            if j not in selected_rows:
                                selected_rows.add(j)
                                break  
                        records = lines[j]
                        new_question = Questions(test = new_test,question = records[0],opt_1 = records[1],opt_2 = records[2],opt_3 = records[3],opt_4 = records[4],right_opt = records[5])
                        new_question.save()               
                messages.success(request, 'Test is arranged successfully!', extra_tags='TestArranged')
        except Exception as e :
            messages.error(request, 'Failed to arrange test :(',extra_tags='TestArrangeFailed')
        
    if 'alter-test-btn' in request.POST:
        try:
            with transaction.atomic():
                subjectID = request.POST.get('subjectID')
                testName = request.POST.get('testName')
                numberOfQuestions = int(request.POST.get('numberOfQuestions'))
                testDate = request.POST.get('testDate')
                testStartTime = request.POST.get('testStartTime')
                testEndTime = request.POST.get('testEndTime')
                prev_test = TestDetails.objects.get(branch=professor.branch,subjectID=subjectID,testName=testName)
                if prev_test.numberOfQuestions == numberOfQuestions :
                    prev_test.DateOfExam = testDate 
                    prev_test.StartTime = testStartTime
                    prev_test.EndTime = testEndTime
                    prev_test.save()
                else :
                    Questions.objects.filter(test=prev_test).delete()
                    prev_test.numberOfQuestions = numberOfQuestions
                    prev_test.DateOfExam = testDate 
                    prev_test.StartTime = testStartTime
                    prev_test.EndTime = testEndTime
                    prev_test.save()
                    obj2 = QuestionBank.objects.get(college=professor.branch.college,subjectID=subjectID)
                    p = 'C:/Users/Lenovo/Desktop/MyProject/edutrack/media/'+str(obj2.questionBank)
                    file = open(p)           
                    csvFile = csv.reader(file)                  
                    lines =[]
                    for i in csvFile:
                        lines.append(i)                    
                    l = len(lines)
                    # Store the indices of selected rows
                    selected_rows= set()
                    for _ in range(numberOfQuestions):
                        while True:
                            j = random.randrange(0, l)
                            if j not in selected_rows:
                                selected_rows.add(j)
                                break  
                        records = lines[j]
                        new_question = Questions(test = new_test,question = records[0],opt_1 = records[1],opt_2 = records[2],opt_3 = records[3],opt_4 = records[4],right_opt = records[5])
                        new_question.save()               
                messages.success(request, 'Test is altered successfully!', extra_tags='TestAltered')
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to alter test :(',extra_tags='TestAlterFailed')

    if 'delete-test-btn' in request.POST:
        try:
            subjectID = request.POST.get('subjectID')
            testName = request.POST.get('testName')
            TestDetails.objects.filter(branch=professor.branch,subjectID=subjectID,testName=testName).delete()
            messages.success(request, 'Test is deleted successfully!', extra_tags='TestDeleted')
        except Exception as e :
            print(e)


    output = {'active_tests':active_tests,'upcoming_tests':upcoming_tests,'subjects':prof_subjects,'prof_upcoming_tests':prof_upcoming_tests}
    return render(request, 'testsHome.html',output)

# HOD Home Page
@csrf_protect
@login_required(login_url='login/')
def hodHome(request):
    hod = HODs.objects.get(email=request.session['username'])
    subjects = SubjectToProfessor.objects.filter(branch=hod.branch)
    professors = Professors.objects.filter(branch=hod.branch)

    if request.method == 'POST':
        # Assign new subject to Professor
        if 'add-subject-btn' in request.POST:
            subjectName  = request.POST.get('subjectName').strip()
            subjectID = request.POST.get('subjectID').strip()
            profemail = request.POST.get('profemail').strip()
            if SubjectToProfessor.objects.filter(branch=hod.branch,subjectID=subjectID).exists() :
                messages.error(request, 'Subject already exists !', extra_tags='AssignSubjectFailed')
            else :
                subject = SubjectToProfessor(branch=hod.branch,subjectName=subjectName,subjectID=subjectID,profemail=profemail)
                subject.save()
            messages.success(request, 'Subject is assigned to professor successfully!', extra_tags='AssignedSubject')

        # Replace assigned subject to Professor
        if 'replace-professor-btn' in request.POST:
            subjectID = request.POST.get('subjectID').strip()
            profemail = request.POST.get('profemail').strip()
            if SubjectToProfessor.objects.filter(branch=hod.branch,subjectID=subjectID,profemail=profemail).exists() :
                messages.error(request, 'Subject is already assigned to this professor !', extra_tags='ReplaceSubjectFailed')
            else:
                subject = SubjectToProfessor.objects.get(branch=hod.branch,subjectID=subjectID)
                subject.profemail = profemail
                subject.save()
                messages.success(request, 'Professor is replaced successfully!', extra_tags='ProfessorReplaced')

        # Delete subject
        if 'remove-subject-btn' in request.POST:
            subjectID = request.POST.get('subjectID').strip()
            subject = SubjectToProfessor.objects.get(branch = hod.branch,subjectID=subjectID)
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
    branch = request.session['branch']
    college = request.session['college']
    college_obj = College.objects.get(name = college)
    branch_obj = Branch.objects.get(branch=branch,college=college_obj)
    subjects = SubjectToProfessor.objects.filter(branch=branch_obj,branch__college=college_obj)
    #subjects = SubjectToProfessor.objects.filter(branch__branch__branch=request.session['branch'],branch__branch__college__name=request.session['college']).order_by('id')
    tests = TestDetails.objects.filter(subjectID__in=subjects.values_list('subjectID', flat=True)).order_by('id')
    current_time = datetime.now()
    active_tests = []
    resume_tests = []
    upcoming_tests = []
    student = Students.objects.get(registrationNum=request.session['username'])
    for test in tests:
        date = test.DateOfExam
        start_time = test.StartTime
        end_time = test.EndTime
        startDatetime = datetime.combine(date, start_time)
        endDatetime = datetime.combine(date, end_time)
        # Add 30 minutes using timedelta
        new_enddatetime = endDatetime + timedelta(minutes=30)

        if StudentScores.objects.filter(test=test,Student=student).exists():
            attempt = StudentScores.objects.get(test=test, Student=student)
            if(startDatetime <= current_time and new_enddatetime >current_time and  attempt.isSubmitted != True) :
                # check if the current date is not greater than DateOfExam for this test
                resume_tests.append(test)
        elif(startDatetime <= current_time and endDatetime > current_time):
            active_tests.append(test)
        elif(startDatetime > current_time):
            upcoming_tests.append(test)
        else :
            pass
    output = {'active_tests':active_tests,'resume_tests':resume_tests,'upcoming_tests':upcoming_tests,}
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
    if StudentScores.objects.filter(Student=student, test=test).exists() :
        # Retrieve the timeRemaining value if the object already exists
        stud_obj = StudentScores.objects.get(Student=student, test=test)
        timeRemaining = stud_obj.TimeRemaining
    else :
        # create the StudentScores object and initialize timeRemaining to the total duration of the test
        stud_obj = StudentScores(Student=student, test=test, startTime=test.StartTime, endTime=test.EndTime,TimeRemaining=duration)
        stud_obj.save()
        timeRemaining = duration
    student_responses = StudentResponses.objects.filter(attempt=stud_obj)
    responses = dict()
    for res in student_responses:
        responses[res.question.id] = res.selectedAnswer

    output = {'final_questions': questions, 'test': test, 'timeRemaining':timeRemaining, 'attempt': stud_obj, 'responses': responses, 'start_time': startDatetime, 'end_time':endDatetime}
    return render(request, 'test-question.html', output)


def testSubmitted(request,test_id):
    if request.method=='POST':
        test = TestDetails.objects.get(id=test_id)
        student = Students.objects.get(registrationNum=request.session['username'])
        studscore = StudentScores.objects.get(test=test, Student=student)
        questions = Questions.objects.filter(test=test).order_by('id')
        studentResponses = StudentResponses.objects.filter(attempt=studscore)
        score=0
        wrong=0
        correct=0
        for q in questions:
            try:
                response = studentResponses.get(question=q)
                if q.right_opt.strip() == response.selectedAnswer.strip():
                    score += 1
                    correct += 1
                else:
                    wrong += 1
            except StudentResponses.DoesNotExist:
                # Handle case where the student did not answer the question
                score = 0
                correct = 0
                wrong = 0
        studscore.isSubmitted = True
        studscore.correctAns = correct
        studscore.wrongAns = wrong
        studscore.score = score
        studscore.save()
        return render(request, 'testSubmitted.html')
    return render(request, 'testSubmitted.html')

@login_required(login_url='/')
def studentResults(request):
    # Retrieve all TestAttempt objects associated with the current student
    Student = Students.objects.get(registrationNum=request.session['username'])
    test_attempts = StudentScores.objects.filter(Student=Student)
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
    professor = Professors.objects.get(email=request.session['username'])
    subjects = SubjectToProfessor.objects.filter(branch  = professor.branch, profemail = request.session['username'])
    submitted_tests = []
    for subject in subjects :
        tests = TestDetails.objects.filter(subjectID=subject.subjectID)
        for test in tests:
            date = test.DateOfExam
            end_time = test.EndTime
            endDatetime = datetime.combine(date, end_time)
            # Add 30 minutes using timedelta
            #new_enddatetime = endDatetime + timedelta(minutes=30)
            if endDatetime < datetime.now(): # check if the current time is not greater than enddatetime  for this test
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
        # Results of students attempted test but not submitted are evaluated.
        if score.isSubmitted == False :
            questions = Questions.objects.filter(test=test).order_by('id')
            studentResponses = StudentResponses.objects.filter(attempt=score)
            scored=0
            wrong=0
            correct=0
            for q in questions:
                try:
                    response = studentResponses.get(question=q)
                    if q.right_opt.strip() == response.selectedAnswer.strip():
                        scored += 1
                        correct += 1
                    else:
                        wrong += 1
                # Handle case where the student did not answer the question
                except StudentResponses.DoesNotExist:
                    scored = 0
                    correct = 0
                    wrong = 0
            score.isSubmitted = True
            score.correctAns = correct
            score.wrongAns = wrong
            score.score = scored
            score.save()
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
