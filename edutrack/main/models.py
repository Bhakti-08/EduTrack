from django.db import models
from django.core import management
from django.utils import timezone
from datetime import timedelta

def default_created_at():
    return timezone.now()

# Create your models here.
class College(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    directoremail = models.CharField(max_length=50)
    semester1_End_date = models.DateField(null=True, blank=True)
    semester2_End_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Branch(models.Model):
    branch = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch
    
class BranchToHOD(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    hodemail = models.CharField(max_length=50)

    def __str__(self):
        return self.branch.branch
    
class SubjectToProfessor(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    subjectID = models.CharField(max_length=20)
    profemail = models.CharField(max_length=50)
    subjectName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.subjectID
    
class QuestionBank(models.Model):
    created_at = models.DateTimeField(default=default_created_at)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    subjectID = models.CharField(max_length=20, default=None)
    questionBank = models.FileField(upload_to='QuestionBanks/',default=None,null=True)

    def delete_old_records(cls):
        six_months_ago = timezone.now() - timedelta(days=6*30)  # Assuming a month has 30 days
        cls.objects.filter(created_at__lt=six_months_ago).delete()

class Directors(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

class Professors(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, default='male')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.firstName + self.lastName

class Students(models.Model):
    registrationNum = models.CharField(max_length=20)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, default='female')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.registrationNum
    
class HODs(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class TestDetails(models.Model):
    created_at = models.DateTimeField(default=default_created_at)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=None)
    subjectID = models.CharField(max_length=20,default=None)
    testName = models.CharField(max_length=20)
    numberOfQuestions = models.IntegerField(default=None)
    DateOfExam = models.DateField(default=None)
    StartTime = models.TimeField(default=None)
    EndTime = models.TimeField(default=None)   

    def delete_old_records(cls):
        six_months_ago = timezone.now() - timedelta(days=6*30)  # Assuming a month has 30 days
        cls.objects.filter(created_at__lt=six_months_ago).delete()

    def __str__(self):
        return self.testName
    
class Questions(models.Model):
    test = models.ForeignKey(TestDetails, on_delete=models.CASCADE, default=None, null=True)
    question = models.TextField()
    opt_1 = models.CharField(max_length=200)
    opt_2 = models.CharField(max_length=200)
    opt_3 = models.CharField(max_length=200)
    opt_4 = models.CharField(max_length=200)
    right_opt = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question
    
class StudentScores(models.Model):
    test = models.ForeignKey(TestDetails, on_delete=models.CASCADE)
    Student = models.ForeignKey(Students, on_delete=models.CASCADE)
    correctAns = models.IntegerField(default=0)
    wrongAns = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    TimeRemaining = models.IntegerField()
    startTime = models.TimeField(default=None)
    endTime = models.TimeField(default=None)
    isSubmitted = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.test.testName + "(" + self.Student.registrationNum + ")")

class StudentResponses(models.Model):
    attempt = models.ForeignKey(StudentScores, on_delete=models.CASCADE, default=None, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, default=None, null=True)
    selectedAnswer = models.CharField(max_length=100)

    def check_question(self, q):
        return self.question == q

    def __str__(self):
        return str(self.question.id) + self.selectedAnswer

