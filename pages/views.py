from django.shortcuts import render, redirect

def index(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')           