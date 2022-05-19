from django.contrib import admin
from .models import  Subject, Student, File ,Activity ,MultipleQuestion ,QuestionandAnswer, Score
from .forms import SubjectForm,StudentForm ,FileForm, ActivityForm ,MultipleQuestionForm ,QuestionandAnswerForm , ScoreForm
from django.contrib.auth.models import  User

class SubjectData(admin.ModelAdmin):
    form = SubjectForm
    list_display = ('subject', 'description','teacher_name',  'timestamp')
    def teacher_name(self, obj):
        try:
            return obj.teacher.get_full_name()
        except:
            return obj.teacher.username

class StudentData(admin.ModelAdmin):
    form = StudentForm
    list_display = ('student_name', 'subjects_list', 'timestamp')
    def student_name(self, obj):
        try:
            return obj.student.get_full_name()
        except:
            return obj.student.username
    def subjects_list(self, obj):
        try:
           return "\n".join([a.subject for a in obj.subject.all()])
        except:
            return "Subjects"
class ActivityData(admin.ModelAdmin):
    form = ActivityForm
    list_display = ('title','subject','teacher_name', 'description', 'is_multiple_choice','is_deployed')
    def teacher_name(self, obj):
        try:
            return obj.teacher.get_full_name()
        except:
            return obj.teacher.username

class FileData(admin.ModelAdmin):
    form = FileForm
    list_display = ('title', 'file', 'subject')

class MultipleQuestionData(admin.ModelAdmin):
    form = MultipleQuestionForm
    list_display = ('question_list', 'activity')
    def question_list(self, obj):
        return 'Question'

class QuestionandAnswerData(admin.ModelAdmin):
    form = QuestionandAnswerForm
    list_display = ('question_list', 'activity')
    def question_list(self, obj):
        return 'Question'


class ScoreData(admin.ModelAdmin):
    form = ScoreForm
    list_display = ('student_name','activity','score','total')
    def student_name(self, obj):
        try:
            return obj.student.get_full_name()
        except:
            return obj.student.username

admin.site.site_header  =  "Admin Portal"  
admin.site.site_title  =  "Admin Dashboard"
admin.site.index_title  =  "Admin Dashboard"

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# @admin.register(User)
class UserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs    
# class UserAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super(UserAdmin, self).get_queryset(request)
#         qs = qs.filter(is_superuser=False)
#         return qs
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subject,SubjectData)
admin.site.register(Student,StudentData)
admin.site.register(File,FileData)
admin.site.register(Activity,ActivityData)
admin.site.register(MultipleQuestion,MultipleQuestionData)
admin.site.register(QuestionandAnswer,QuestionandAnswerData)
admin.site.register(Score,ScoreData)