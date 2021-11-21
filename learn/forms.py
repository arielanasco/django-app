from django import forms
from django.contrib.auth.models import User
from .models import  Subject
TEACHERS = User.objects.filter(is_staff=True,is_active=True)
STUDENTS =  User.objects.filter(is_staff=False,is_active=True)
SUBJECTS = Subject.objects.all()

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name

class SubjectForm(forms.ModelForm):
    subject = forms.CharField(required=True)
    image = forms.FileField(label='Subject Image', required=True)
    description = forms.CharField(required=True)
    teacher = MyModelChoiceField(queryset=TEACHERS,required=True)


class StudentForm(forms.ModelForm):
    student = MyModelChoiceField(queryset=STUDENTS,required=True)
    subject = forms.ModelChoiceField(queryset=SUBJECTS,required=True)

