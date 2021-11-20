from django import forms
from django.contrib.auth.models import User
from .models import  Subject
TEACHERS = User.objects.filter(is_staff=True,is_active=True)
STUDENTS =  User.objects.filter(is_staff=False,is_active=True)
SUBJECTS = Subject.objects.all()
class SubjectForm(forms.ModelForm):
    subject = forms.CharField(required=True)
    image = forms.FileField(label='Subject Image', required=True)
    description = forms.CharField(required=True)
    teacher = forms.ModelChoiceField(queryset=TEACHERS,required=True)

class StudentForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=STUDENTS,required=True)
    subject1 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject2 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject3 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject4 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject5 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject6 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject7 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
    subject8 = forms.ModelChoiceField(queryset=SUBJECTS,required=False)
