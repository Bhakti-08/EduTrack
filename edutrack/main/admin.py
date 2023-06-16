from django.contrib import admin
from . import models

# Register your models here.
class DirectorsAdmin(admin.ModelAdmin):
    readonly_fields = ['name','gender','college','email']
    list_display = ['name','gender','college','email']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.Directors,DirectorsAdmin)

class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name','directoremail','semester1_End_date','semester2_End_date']
admin.site.register(models.College,CollegeAdmin)

class BranchAdmin(admin.ModelAdmin):
    readonly_fields = ['branch','college']
    list_display = ['branch','college']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.Branch,BranchAdmin)

class BranchToHODAdmin(admin.ModelAdmin):
    readonly_fields = ['branch','hodemail']
    list_display = ['branch','hodemail']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.BranchToHOD,BranchToHODAdmin)

class SubjectToProfessorAdmin(admin.ModelAdmin):
    readonly_fields = ['branch','subjectID','subjectName','profemail']
    list_display = ['branch','subjectID','subjectName','profemail']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.SubjectToProfessor,SubjectToProfessorAdmin)

class QuestionBankAdmin(admin.ModelAdmin):
    readonly_fields = ['college','subjectID','questionBank']
    list_display = ['college','subjectID','questionBank']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.QuestionBank,QuestionBankAdmin)

class HODsAdmin(admin.ModelAdmin):
    readonly_fields = ['name','email','branch']
    list_display = ['name','email','branch']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.HODs,HODsAdmin)

class ProfessorsAdmin(admin.ModelAdmin):
    readonly_fields = ['firstName','lastName','email','branch',]
    list_display = ['firstName','lastName','email','branch',]
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.Professors,ProfessorsAdmin)

class StudentsAdmin(admin.ModelAdmin):
    readonly_fields = ['registrationNum','firstName','lastName']
    list_display = ['registrationNum','firstName','lastName']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
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
    readonly_fields = ['test', 'Student','correctAns','wrongAns','score','TimeRemaining','startTime', 'endTime']
    list_display = ['test', 'Student','correctAns','wrongAns','score','TimeRemaining','startTime', 'endTime']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(models.StudentScores, StudentScoresAdmin)