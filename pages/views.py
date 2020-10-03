from django.shortcuts import render, redirect

def index(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html') 

def projects(request):
    return render(request, 'projects/home.html') 

def dashboard(request):
    return render(request, 'pages/dashboard.html')                