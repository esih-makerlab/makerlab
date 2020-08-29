from django.shortcuts import render, redirect

def home(request):
    return render(request, 'page/home.html')

def index(request):
    return redirect( 'home')

def membership(request):
    return render(request, 'page/membership.html')

def cours(request):
    return render(request, 'page/cours.html') 

def about(request):
    return render(request, 'page/about.html')           