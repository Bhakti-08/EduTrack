from django.contrib import admin
from . import models

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch']
admin.site.register(models.Branch,BranchAdmin)

class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['branch','subjectID','subjectName']
admin.site.register(models.Subjects,SubjectsAdmin)

class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ['subjectID','questionBank']
admin.site.register(models.QuestionBank,QuestionBankAdmin)

class ProfessorsAdmin(admin.ModelAdmin):
    list_display = ['firstName','lastName','email','branch','subjectID']
admin.site.register(models.Professors,ProfessorsAdmin)

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['registrationNum','firstName','lastName']
admin.site.register(models.Students,StudentsAdmin)

class TestDetailsAdmin(admin.ModelAdmin):
    list_display = ['branch','subject','testName','DateOfExam', 'StartTime','EndTime']
admin.site.register(models.TestDetails,TestDetailsAdmin)

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['test','question']
admin.site.register(models.Questions,QuestionsAdmin)

class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['test', 'student', 'startTime', 'endTime']
admin.site.register(models.TestAttempt,TestAttemptAdmin)

class StudentResponsesAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selectedAnswer']
admin.site.register(models.StudentResponses,StudentResponsesAdmin)