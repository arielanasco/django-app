from re import sub
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject,Student,File
from django.contrib.auth.models import User
from .forms import FileForm


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
        if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                title= form.cleaned_data.get("title")
                form.save()
                messages.success(request,f"File {title} uploaded successfully...")
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            form = FileForm(initial={'subject':subject.subject,'teacher':request.user.get_full_name()})
            files = File.objects.filter(subject=subject.subject)
        return render(request, 'learn/teacher/view.html', {'subject':subject,'files':files,'form':form})
    return render(request, 'learn/student/view.html', {'subject':subject})

def delete_file(request,id):
    file = File.objects.get(id=id)
    file.delete()
    messages.success(request,"File deleted successfully...")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request):
    return render(request, 'learn/common/profile.html')



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