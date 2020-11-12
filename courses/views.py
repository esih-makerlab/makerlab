from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model
from django.http import Http404

from .models import Course,CourseDate

def home(request):
        
    page = request.GET.get('page', 1)
        
    paginator = Paginator(Course.objects.all(), 3)

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'courses/home.html',{'courses':courses})           

def course_details(request,id):
    return render(request, 'courses/detail.html')

def course_enrollement(request,id):

    try:
        courseDate = CourseDate.objects.get(pk=id)
    except CourseDate.DoesNotExist:
        raise Http404("Not found.")

    return render(request, 'courses/enrollement.html',{'courseDate':courseDate})

def course_payement(request):
    return render(request, 'courses/payement.html')

def search_results(request):
    q = request.GET.get('q','')

    courses =  Course.objects.annotate(search = SearchVector('title','description')).filter(search__icontains=q)[:25]

    return render(request, 'courses/search_results.html',{'courses':courses,'q':q})