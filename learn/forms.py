from django import forms
from django.contrib.auth.models import User
from .models import Subject, Student, File , Activity
from django.contrib.admin import widgets

TEACHERS = User.objects.filter(is_staff=True,is_active=True)
STUDENTS =  User.objects.filter(is_staff=False,is_active=True)
SUBJECTS = Subject.objects.all()
class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['timestamp'].widget = widgets.AdminSplitDateTime()
        TEACHERS = User.objects.filter(is_staff=True,is_active=True)
        self.fields['teacher'].choices = [(user.pk, user.get_full_name()) for user in TEACHERS]

    class Meta:
        model = Subject
        fields = ('subject','image','description','teacher','timestamp')

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['timestamp'].widget = widgets.AdminSplitDateTime()
        STUDENTS =  User.objects.filter(is_staff=False,is_active=True)
        self.fields['student'].choices = [(user.pk, user.get_full_name()) for user in STUDENTS]

    class Meta:
        model = Student
        fields = ('student','subject','timestamp')



class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        SUBJECTS = Subject.objects.all()
        self.fields['subject'].choices = [(subject.pk, subject.subject) for subject in SUBJECTS]
        self.fields['teacher'].choices = [(user.pk, user.get_full_name()) for user in TEACHERS]
        self.fields['is_multiple_choice'].help_text = "Uncheck this for Question and Answer type"

    class Meta:
        model = Activity
        fields = ('subject','title','description','teacher', 'is_multiple_choice','is_deployed')
    
class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        SUBJECTS = Subject.objects.all()
        TEACHERS = User.objects.filter(is_staff=True,is_active=True)
        self.fields['teacher'].choices = [(user.pk, user.get_full_name()) for user in TEACHERS]
        self.fields['subject'].choices = [(subject.id, subject.subject) for subject in SUBJECTS]

    class Meta:
        model = File
        fields = ('subject','title','description','file','teacher')


