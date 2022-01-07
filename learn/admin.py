from django.contrib import admin
from .models import  Subject, Student, File ,Activity ,MultipleQuestion ,QuestionandAnswer, QuestionandAnswerSheet
from .forms import SubjectForm,StudentForm ,FileForm, ActivityForm ,MultipleQuestionForm ,QuestionandAnswerForm ,QuestionandAnswerSheetForm
from django.contrib.auth.models import Group

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
    list_display = ('student_name', 'subject', 'timestamp')
    def student_name(self, obj):
        try:
            return obj.student.get_full_name()
        except:
            return obj.student.username

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

class QuestionandAnswerSheetData(admin.ModelAdmin):
    form = QuestionandAnswerSheetForm
    list_display = ('question_list', 'answer')
    def question_list(self, obj):
        return 'User Answer'
            
admin.site.site_header  =  "IMath Admin Portal"  
admin.site.site_title  =  "IMath Admin Dashboard"
admin.site.index_title  =  "IMath Admin Dashboard"


admin.site.unregister(Group)
admin.site.register(Subject,SubjectData)
admin.site.register(Student,StudentData)
admin.site.register(File,FileData)
admin.site.register(Activity,ActivityData)
admin.site.register(MultipleQuestion,MultipleQuestionData)
admin.site.register(QuestionandAnswer,QuestionandAnswerData)
admin.site.register(QuestionandAnswerSheet,QuestionandAnswerSheetData)