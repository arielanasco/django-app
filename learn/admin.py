from django.contrib import admin
from .models import Profile, Subject, Student, File
from .forms import SubjectForm,StudentForm ,FileForm
from django.contrib.auth.models import Group

class SubjectData(admin.ModelAdmin):
    form = SubjectForm
    list_display = ('teacher_name', 'subject', 'description', 'timestamp')
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

class FileData(admin.ModelAdmin):
    form = FileForm
    list_display = ('title', 'file', 'subject')


            
admin.site.site_header  =  "IMath Admin Portal"  
admin.site.site_title  =  "IMath Admin Dashboard"
admin.site.index_title  =  "IMath Admin Dashboard"


admin.site.register(Profile)
admin.site.unregister(Group)
admin.site.register(Subject,SubjectData)
admin.site.register(Student,StudentData)
admin.site.register(File,FileData)
