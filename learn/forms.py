from django import forms
from django.contrib.auth.models import User
from .models import  Subject, File , Activity
from django.contrib.admin import widgets

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

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['timestamp'].widget = widgets.AdminSplitDateTime()

class StudentForm(forms.ModelForm):
    student = MyModelChoiceField(queryset=STUDENTS,required=True)
    subject = forms.ModelChoiceField(queryset=SUBJECTS,required=True)

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['timestamp'].widget = widgets.AdminSplitDateTime()

class ActivityForm(forms.ModelForm):
    subject =   forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'subject','readonly':'true'}))
    title =   forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'title'}))
    description =  forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'description', 'id':'description'}))
    teacher = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'teacher','readonly':'true'}))
    is_multiple_choice =  forms.BooleanField(required=True,initial=True, widget=forms.CheckboxInput({'class': 'form-check-input','type':'checkbox', 'id':'is_multiple_choice'}),help_text="Uncheck this for Question and Answer type")
    is_deployed =  forms.BooleanField(initial=False,label="Deploy?")

    class Meta:
        model = Activity
        fields = ('subject','title','description','teacher', 'is_multiple_choice','is_deployed')
    
class FileForm(forms.ModelForm):
    subject =  forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'subject'}))
    title =  forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'title'}))
    description =  forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'description', 'id':'description'}))
    teacher =  forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','type':'text', 'id':'teacher'}))

    class Meta:
        model = File
        fields = ('subject','title','description','file','teacher')



