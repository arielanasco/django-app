from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin

# Create your views here.


def home(request):
    if request.user.is_staff:
        return render(request, 'learn/teacher/home.html')    
    return render(request, 'learn/student/home.html')
