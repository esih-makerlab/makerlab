from django.shortcuts import render, redirect

def index(request):
    return redirect('/courses')

def about(request):
    return render(request, 'page/about.html')           