from re import sub
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject,Student,File,Activity ,MultipleQuestion, QuestionandAnswer, Score
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm, FileForm, ActivityForm, MultipleQuestionForm, QuestionandAnswerForm, QuestionandAnswerSheetForm
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form.fields['username'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'username' ,'aria-describedby':'inputGroup-sizing-sm-username'})
        u_form.fields['email'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'email' ,'aria-describedby':'inputGroup-sizing-sm-email'})
        u_form.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'first_name' ,'aria-describedby':'inputGroup-sizing-sm-fname'})
        u_form.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'last_name' ,'aria-describedby':'inputGroup-sizing-sm-lname'})
        p_form.fields['image'].widget.attrs.update({'class': 'form-control form-control-sm','type':'file', 'id':'image'})

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f"Profile updated successfully...")
            return redirect('profile')
        else:
            for error_u_field in u_form.errors:
                messages.error(request,f"There is an error in the {error_u_field} field")
            for error_p_field in p_form.errors:
                messages.error(request,f"There is an error in the {error_p_field} field")
            return redirect('profile')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    u_form.fields['username'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'username' ,'aria-describedby':'inputGroup-sizing-sm-username'})
    u_form.fields['email'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'email' ,'aria-describedby':'inputGroup-sizing-sm-email'})
    u_form.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'first_name' ,'aria-describedby':'inputGroup-sizing-sm-fname'})
    u_form.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-sm','type':'text', 'id':'last_name' ,'aria-describedby':'inputGroup-sizing-sm-lname'})
    p_form.fields['image'].widget.attrs.update({'class': 'form-control form-control-sm','type':'file', 'id':'image'})

    if request.user.is_staff:
        subjects = Subject.objects.filter(teacher=request.user)
        scores = Score.objects.filter(activity__teacher=request.user)
        context ={
            'u_form':u_form,
            'p_form':p_form,
            'subjects':subjects,
            'scores':scores
        }
        return render(request, 'learn/common/profile.html', context)  

    scores = Score.objects.filter(student=request.user)
    context ={
        'u_form':u_form,
        'p_form':p_form,
        'scores' :scores
    }
    return render(request, 'learn/common/profile.html', context)

@login_required
def home(request):
    user = User.objects.get(username=request.user.get_username())
    if request.user.is_staff:
        subjects = Subject.objects.filter(teacher_id=user.id)
        return render(request, 'learn/teacher/home.html', {'subjects':subjects})
    subjects = Student.objects.filter(student = user.id)
    return render(request, 'learn/student/home.html', {'subjects':subjects})

@login_required
def view_subject(request,id):
    subject = Subject.objects.get(id=id)
    if request.user.is_staff:
        if request.method == 'POST' and request.POST.get("file_upload"):
            form_upload = FileForm(request.POST, request.FILES)
            if form_upload.is_valid():
                title= form_upload.cleaned_data.get("title")
                form_upload.save()
                messages.success(request,f"File {title} uploaded successfully...")
                return redirect(request.META.get('HTTP_REFERER'))
        if request.method == 'POST' and request.POST.get("create_activity"):
            form_activity = ActivityForm(request.POST)
            if form_activity.is_valid():
                title= form_activity.cleaned_data.get("title")
                form_activity.save()
                messages.success(request,f"Activity {title} created  successfully...")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                pass
                # print(form_activity.errors)

        form_upload = FileForm(initial={'subject':subject.id,'teacher':request.user.id})
        form_upload.fields['subject'].widget.attrs['hidden'] = True
        form_upload.fields['teacher'].widget.attrs['hidden'] = True
        form_upload.fields['title'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'title'})
        form_upload.fields['description'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'description'})
        form_upload.fields['file'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'file'})

        form_activity = ActivityForm(initial={'subject':subject.id,'teacher':request.user.id,'is_deployed':'false'})
        form_activity.fields['subject'].widget.attrs['hidden'] = True
        form_activity.fields['teacher'].widget.attrs['hidden'] = True
        form_activity.fields['is_deployed'].widget.attrs['hidden'] = True
        form_activity.fields['title'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'title'})
        form_activity.fields['description'].widget.attrs.update({'class': 'form-control','type':'text', 'id':'description'})
        form_activity.fields['is_deployed'].widget.attrs.update({'class': 'form-check-input','type':'checkbox', 'id':'file'})
        files = File.objects.filter(subject=subject.id)
        activities = Activity.objects.filter(subject=subject.id)
        return render(request, 'learn/teacher/view.html', {'subject':subject, 'activities': activities,'files':files,'form_upload':form_upload,'form_activity':form_activity})
    ans_act = Score.objects.filter(student=request.user).values_list('activity', flat=True)
    activities = Activity.objects.filter(subject=subject.id, is_deployed=True).exclude(id__in=ans_act)
    files = File.objects.filter(subject=subject.id)
    return render(request, 'learn/student/view.html', {'subject':subject,'files':files, 'activities':activities})

def delete_file(request,id):
    if request.user.is_staff:
        file = File.objects.get(id=id)
        file.delete()
        messages.success(request,"File deleted successfully...")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request,f"You are not allowed to do it...")
    return redirect(request.META.get('HTTP_REFERER'))

def delete_activity(request,id):
    if request.user.is_staff:
        activity = Activity.objects.get(id=id)
        activity.delete()
        messages.success(request,"Activity deleted successfully...")
        return redirect('learn-home')    
    messages.error(request,f"You are not allowed to do it...")
    return redirect('learn-home')

@login_required
def download_file(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    messages.error(request,f"File {file_path} is deleted...")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def upload_file(request):
    if request.user.is_staff:
        # messages.success(request,"File uploaded successfully...")
        return render(request, 'learn/teacher/upload_file.html')

    messages.error(request,"You are not allowed to access it.")
    return redirect('learn-home')

@login_required
def create_activity(request,id):
    try:
        activity = Activity.objects.get(id=id)
        if request.user.is_staff:
            if activity.is_multiple_choice:
                if request.method == 'POST':
                    form_question = MultipleQuestionForm(request.POST)
                    if form_question.is_valid() and request.POST.get('option'):
                        messages.success(request,"Question added successfully!")
                        form_question = form_question.save()
                        form_question.ans = request.POST.get('option')
                        form_question.save()
                    else:
                        messages.error(request,"Error! Unable to save it.")
                    return redirect(request.META.get('HTTP_REFERER'))
                questions = MultipleQuestion.objects.filter(activity=activity.id)
                form = MultipleQuestionForm(initial={'activity':activity.id,'ans':"A",'ans_exp':"None"})
                form.fields['activity'].widget.attrs['hidden'] = True
                form.fields['ans'].widget.attrs['hidden'] = True
                form.fields['question'].widget.attrs.update({'type':'text','class':'form-control','id':'question'})
                form.fields['choice_a'].widget.attrs.update({'type':'text','class':'form-control','id':'choice_a'})
                form.fields['choice_b'].widget.attrs.update({'type':'text','class':'form-control','id':'choice_b'})
                form.fields['choice_c'].widget.attrs.update({'type':'text','class':'form-control','id':'choice_c'})
                form.fields['choice_d'].widget.attrs.update({'type':'text','class':'form-control','id':'choice_d'})
                form.fields['ans_exp'].widget.attrs.update({'type':'text','class':'form-control','id':'ans_exp'})
            else:
                if request.method == 'POST':
                    form_question = QuestionandAnswerForm(request.POST)
                    if form_question.is_valid():
                        messages.success(request,"Question added successfully!")
                        form_question.save()
                    else:
                        messages.error(request,"Error! Unable to save this.")
                    return redirect(request.META.get('HTTP_REFERER'))
                questions = QuestionandAnswer.objects.filter(activity=activity.id)
                form = QuestionandAnswerForm(initial={'activity':activity.id})
                form.fields['activity'].widget.attrs['hidden'] = True
                form.fields['question'].widget.attrs.update({'type':'text','class':'form-control','id':'question'})
            return render(request, 'learn/teacher/create_activity.html' , {'questions':questions, 'activity':activity, 'form':form})
        messages.error(request,"You are not allowed to access it.")
        return redirect('learn-home')
    except ObjectDoesNotExist:
        messages.error(request,"Activity does not exist.")
        return redirect('learn-home')

@login_required
def deploy_activity(request,id):
    activity = Activity.objects.get(id=id)
    if activity.is_deployed:
        activity.is_deployed=False
        activity.save()
        messages.info(request,"Activity was not deployed.")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        activity.is_deployed=True
        activity.save()        
        messages.success(request,"Activity is deployed.")
        return redirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_question(request,mode,id):
    if mode:
        question = MultipleQuestion.objects.get(id=id)
        messages.success(request,f"Question #{question.id} is deleted.")
        question.delete()
    else:
        question = QuestionandAnswer.objects.get(id=id)
        messages.success(request,f"Question #{question.id} is deleted.")
        question.delete()    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def answer_activity(request,id):
    activity = Activity.objects.get(id=id)
    if request.method == 'POST':
        if activity.is_multiple_choice:
            answers = MultipleQuestion.objects.filter(activity=activity.id).values_list('id','ans')
            ctr = 0
            for key in answers:
                user_answer  = request.POST.get(f'option{key[0]}')
                if user_answer == key[1]:
                    ctr += 1
            if Score.objects.filter(activity=activity, student=request.user):
                messages.error(request,"You answered it already!")
                return redirect('profile')
            else:
                user_score = Score(activity=activity, student=request.user, score=ctr, total=len(answers))
                user_score.save()
                messages.error(request,"Score recorded")
                return redirect('profile')
            # try:
            #     user_score = Score.objects.get(activity=activity, student=request.user)
            #     user_score.score=ctr
            #     user_score.save()
            # except:
            #     user_score = Score(activity=activity, student=request.user, score=ctr, total=len(answers))
            #     user_score.save()
            # return redirect('profile')
        else:
            messages.error(request,"Question and Answer option is not available now")
            return redirect('profile')
    
    if activity.is_multiple_choice:
        questions = MultipleQuestion.objects.filter(activity=activity.id)
        context = {
            'activity': activity,
            'questions' : questions
        }
        return render(request, 'learn/student/answer-activity.html' , context)
    else:
        questions = QuestionandAnswer.objects.filter(activity=activity.id).values_list('question')
        QuestionandAnswerSheetFormSet = formset_factory(QuestionandAnswerSheetForm, extra=len(questions))
        formset = QuestionandAnswerSheetFormSet()
        context = {
            'activity': activity,
            'formset': formset
        }
        return render(request, 'learn/student/answer-activity.html' , context)
