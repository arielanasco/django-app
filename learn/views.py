from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
contexts  = [
    {'subject': 'Mathematics of the Modern World', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'Science and Technology', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'College Algebra', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'College Algebra', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'College Algebra', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'College Algebra', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
    {'subject': 'College Algebra', 'desc':'This is a wider card with supporting text below as a natural lead-in to additional content.'},
]

@login_required
def home(request):
    if request.user.is_staff:
        return render(request, 'learn/teacher/home.html', {'contexts':contexts})    
    return render(request, 'learn/student/home.html', {'contexts':contexts})

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