from re import sub
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject,Student
from django.contrib.auth.models import User

@login_required
def home(request):
    user = User.objects.get(username=request.user.get_username())
    if request.user.is_staff:
        subjects = Subject.objects.filter(teacher_id=user.id)
        return render(request, 'learn/teacher/home.html', {'subjects':subjects})
    subjects = Student.objects.filter(student_id = user.id)
    return render(request, 'learn/student/home.html', {'subjects':subjects})

@login_required
def view_subject(request):
    if request.user.is_staff:
        messages.info(request,"You are not allowed to access it.")
        return redirect('learn-home')
    return render(request, 'learn/student/view.html')

@login_required
def profile(request):
    return render(request, 'learn/common/profile.html')

@login_required
def upload_file(request):
    if request.user.is_staff:
        return render(request, 'learn/teacher/upload_file.html')
    messages.info(request,"You are not allowed to access it.")

    return redirect('learn-home')

@login_required
def create_activity(request):
    if request.user.is_staff:
        return render(request, 'learn/teacher/create_activity.html')
    messages.info(request,"You are not allowed to access it.")
    return redirect('learn-home')