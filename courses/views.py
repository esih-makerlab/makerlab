from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model

from .models import Course

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

def course_enrollement(request):
    return render(request, 'courses/enrollement.html')

def course_payement(request):
    return render(request, 'courses/payement.html')

def search_results(request):
    q = request.GET.get('q','')

    filter_search = request.GET.get('filter')

    if not filter_search:
        filter_search = 'course'

    courses = None
    teachers = None

    if filter_search == 'teacher':
        teachers =  get_user_model().objects.annotate(search = SearchVector('first_name','last_name')).filter(search__icontains=q,is_teacher=True)
    else:
        courses =  Course.objects.annotate(search = SearchVector('title','description')).filter(search__icontains=q)

    return render(request, 'courses/search_results.html',{'courses':courses,'teachers':teachers,'filter':filter_search,'q':q})