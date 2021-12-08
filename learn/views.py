from re import sub
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject,Student,File,Activity
from django.contrib.auth.models import User
from .forms import FileForm ,ActivityForm
import os
from django.conf import settings
from django.http import HttpResponse, Http404

@login_required
def home(request):
    user = User.objects.get(username=request.user.get_username())
    if request.user.is_staff:
        subjects = Subject.objects.filter(teacher_id=user.id)
        return render(request, 'learn/teacher/home.html', {'subjects':subjects})
    subjects = Student.objects.filter(student_id = user.id)
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
                print(form_activity)
                print("you didnt clicked the create activity")

        form_upload = FileForm(initial={'subject':subject.subject,'teacher':request.user.get_full_name()})
        form_upload.fields['subject'].widget.attrs['readonly'] = True
        form_upload.fields['teacher'].widget.attrs['readonly'] = True
        form_activity = ActivityForm(initial={'subject':subject.subject,'teacher':request.user.get_full_name(),'is_deployed':'true'})
        form_activity.fields['subject'].widget.attrs['readonly'] = True
        form_activity.fields['teacher'].widget.attrs['readonly'] = True
        form_activity.fields['is_deployed'].widget.attrs['hidden'] = True
        files = File.objects.filter(subject=subject.subject)
        activities = Activity.objects.filter(subject=subject.subject)
        return render(request, 'learn/teacher/view.html', {'subject':subject, 'activities': activities,'files':files,'form_upload':form_upload,'form_activity':form_activity})
    files = File.objects.filter(subject=subject.subject)
    return render(request, 'learn/student/view.html', {'subject':subject,'files':files})

def delete_file(request,id):
    if request.user.is_staff:
        file = File.objects.get(id=id)
        file.delete()
        messages.success(request,"File deleted successfully...")
        return redirect(request.META.get('HTTP_REFERER'))
    messages.error(request,f"You are not allowed to do it...")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    return render(request, 'learn/common/profile.html')

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
def create_activity(request):
    if request.user.is_staff:
        # messages.info(request,'Created activity successfully... Click here to start inserting items <a href="#">here</a> >')
        return render(request, 'learn/teacher/create_activity.html')
    messages.error(request,"You are not allowed to access it.")
    return redirect('learn-home')