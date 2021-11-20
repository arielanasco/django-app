from django.contrib import admin
from .models import Profile, Subject, Student
from .forms import SubjectForm,StudentForm
from django.contrib.auth.models import Group

class SubjectData(admin.ModelAdmin):
    form = SubjectForm
    list_display = ('subject', 'description', 'teacher')

class StudentData(admin.ModelAdmin):
    form = StudentForm
    list_display = ('student', 'subject1',  'subject2', 'subject3', 'subject4', 'subject5', 'subject6', 'subject7', 'subject8',)

admin.site.site_header  =  "IMath Admin Portal"  
admin.site.site_title  =  "IMath Admin Dashboard"
admin.site.index_title  =  "IMath Admin Dashboard"


admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.register(Subject,SubjectData)
admin.site.register(Student,StudentData)
