from django.contrib import admin
from . import models

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch']
admin.site.register(models.Branch,BranchAdmin)

'''class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['branch','subjectID','subjectName']
admin.site.register(models.Subjects,SubjectsAdmin)'''

class SubjectToProfessorAdmin(admin.ModelAdmin):
    list_display = ['branch','subjectID','subjectName','profemail']
admin.site.register(models.SubjectToProfessor,SubjectToProfessorAdmin)

class QuestionBankAdmin(admin.ModelAdmin):
    readonly_fields = ['subjectID','questionBank']
    list_display = ['subjectID','questionBank']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.QuestionBank,QuestionBankAdmin)

class HODsAdmin(admin.ModelAdmin):
    list_display = ['name','email','branch']
admin.site.register(models.HODs,HODsAdmin)

class ProfessorsAdmin(admin.ModelAdmin):
    list_display = ['firstName','lastName','email','branch',]
admin.site.register(models.Professors,ProfessorsAdmin)

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['registrationNum','firstName','lastName']
admin.site.register(models.Students,StudentsAdmin)

class TestDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ['branch','subjectID','testName','DateOfExam', 'StartTime','EndTime']
    list_display = ['branch','subjectID','testName','DateOfExam', 'StartTime','EndTime']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.TestDetails,TestDetailsAdmin)

class QuestionsAdmin(admin.ModelAdmin):
    readonly_fields = ['test','question']
    list_display = ['test','question']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.Questions,QuestionsAdmin)

class TestAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ['test', 'student', 'startTime', 'endTime']
    list_display = ['test', 'student', 'startTime', 'endTime']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.TestAttempt,TestAttemptAdmin)

class StudentResponsesAdmin(admin.ModelAdmin):
    readonly_fields = ['attempt', 'question', 'selectedAnswer']
    list_display = ['attempt', 'question', 'selectedAnswer']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.StudentResponses,StudentResponsesAdmin)

class StudentScoresAdmin(admin.ModelAdmin):
    readonly_fields = ['test', 'Student','correctAns','wrongAns','score','TimeRemaining']
    list_display = ['test', 'Student','correctAns','wrongAns','score','TimeRemaining']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.StudentScores, StudentScoresAdmin)