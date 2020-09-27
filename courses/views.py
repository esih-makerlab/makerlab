from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Courses


def home(request):
        
    page = request.GET.get('page', 1)
        
    paginator = Paginator(Courses.objects.all(), 1)

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'courses/home.html',{'courses':courses})           