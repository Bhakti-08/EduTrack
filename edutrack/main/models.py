from django.db import models
from django.core import management

# Create your models here.
class Branch(models.Model):
    branch = models.CharField(max_length=100)

    def __str__(self):
        return self.branch

class Subjects(models.Model):
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE)
    subjectID = models.CharField(max_length=20)
    subjectName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.subjectName

class QuestionBank(models.Model):
    subjectID = models.CharField(max_length=20, default=None)
    questionBank = models.FileField(upload_to='QuestionBanks/',default=None,null=True)

class Professors(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    #subject = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    subjectID = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.firstName + self.subjectID

class Students(models.Model):
    registrationNum = models.CharField(max_length=20)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.registrationNum
    
class TestDetails(models.Model):
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, default=None)
    subject = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    testName = models.CharField(max_length=20)
    numberOfQuestions = models.IntegerField(default=None)
    DateOfExam = models.DateField(default=None)
    StartTime = models.TimeField(default=None)
    EndTime = models.TimeField(default=None)   

    def __str__(self):
        return self.testName
    
class Questions(models.Model):
    #subject = models.ForeignKey(Subjects, on_delete = models.CASCADE, default=None, null=True)
    # means if this category is terminated then all questions related to this category will also get deleted
    #subject = models.CharField(max_length=100)
    test = models.ForeignKey(TestDetails, on_delete=models.CASCADE, default=None, null=True)
    question = models.TextField()
    opt_1 = models.CharField(max_length=200)
    opt_2 = models.CharField(max_length=200)
    opt_3 = models.CharField(max_length=200)
    opt_4 = models.CharField(max_length=200)
    right_opt = models.CharField(max_length=100)
    
    def __str__(self):
        return self.question
    
class TestAttempt(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    test = models.ForeignKey(TestDetails, on_delete=models.CASCADE)
    startTime = models.TimeField(default=None)
    endTime = models.TimeField(default=None)
    isSubmitted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.test.testName + "(" + self.student.registrationNum + ")")


class StudentResponses(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, default=None, null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, default=None, null=True)
    selectedAnswer = models.CharField(max_length=100)

    def check_question(self, q):
        return self.question == q

    def __str__(self):
        return str(self.question.id) + self.selectedAnswer
    

class StudentScores(models.Model):
    test = models.ForeignKey(TestDetails, on_delete=models.CASCADE)
    Student = models.ForeignKey(Students, on_delete=models.CASCADE)
    correctAns = models.IntegerField(default=0)
    wrongAns = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    TimeRemaining = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.score)