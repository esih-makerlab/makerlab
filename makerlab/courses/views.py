from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model
from django.http import Http404,HttpResponse

from django.contrib.auth.decorators import login_required

from .models import Course,CourseDate,Attendee


def home(request):
        
    page = request.GET.get('page', 1)
        
    paginator = Paginator(Course.objects.all().order_by("title"), 3)
    courses = None
    
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'courses/home.html',{'courses':courses})           

def course_details(request,id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Not found.")

    return render(request, 'courses/detail.html',{'course':course})

@login_required(login_url='/account/login')
def course_enrollement(request,id):

    try:
        courseDate = CourseDate.objects.get(pk=id)
    except CourseDate.DoesNotExist:
        raise Http404("Not found.")

    try:
        attendee = Attendee.objects.get(start_date=courseDate,attendee=request.user)
    except Attendee.DoesNotExist:
        attendee = None
    
    if attendee:
        return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'enrolled':True,'soldOut':False})

    if courseDate.remainPlaces <= 0:
        return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'soldOut':True})


    return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'soldOut':False})     

def search_results(request):
    q = request.GET.get('q','')

    courses =  Course.objects.annotate(search = SearchVector('title','description'))
    if courses ==  q :
        courses =courses.filter(title__contains=q)[:25]
    else:
        courses =courses.filter(title__icontains=q)[:25]
    return render(request, 'courses/search_results.html',{'courses':courses,'q':q})