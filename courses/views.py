from django.shortcuts import render, redirect

def home(request):
    return render(request, 'courses/home.html')           

def course_details(request):
    return render(request, 'courses/detail.html')