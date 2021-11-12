from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    if request.user.is_staff:
        return render(request, 'learn/teacher/home.html')    
    return render(request, 'learn/student/home.html')
