from django import forms
from .models import  Profile, Subject, Student, File , Activity , MultipleQuestion, QuestionandAnswer ,QuestionandAnswerSheet
from django.contrib.admin import widgets
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



TEACHERS = User.objects.filter(is_staff=True,is_active=True)
STUDENTS =  User.objects.filter(is_staff=False,is_active=True)
SUBJECTS = Subject.objects.all()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email' ,'first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

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


class MultipleQuestionForm(forms.ModelForm):
    question = forms.CharField(widget=CKEditorUploadingWidget())

    def __init__(self, *args, **kwargs):
        super(MultipleQuestionForm, self).__init__(*args, **kwargs)
        activities = Activity.objects.all()
        self.fields['activity'].choices = [(activity.pk, activity.title) for activity in activities]

    class Meta:
        model = MultipleQuestion
        fields = '__all__'
        exclude = ("timestamp",)


class QuestionandAnswerForm(forms.ModelForm):
    question = forms.CharField(widget=CKEditorUploadingWidget())

    def __init__(self, *args, **kwargs):
        super(QuestionandAnswerForm, self).__init__(*args, **kwargs)
        activities = Activity.objects.all()
        self.fields['activity'].choices = [(activity.pk, activity.title) for activity in activities]

    class Meta:
        model = QuestionandAnswer
        fields = '__all__'
        exclude = ("timestamp",)

class QuestionandAnswerSheetForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorUploadingWidget())

    def __init__(self, *args, **kwargs):
        super(QuestionandAnswerSheetForm, self).__init__(*args, **kwargs)
        questions = QuestionandAnswer.objects.all()
        self.fields['question'].choices = [(question.pk, question.question) for question in questions]
        self.fields['question'].widget.attrs.update({'type':'text','class':'form-control','id':'question'})

    class Meta:
        model = QuestionandAnswerSheet
        fields = '__all__'
        exclude = ("timestamp",)