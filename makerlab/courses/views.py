from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model
from django.http import Http404,HttpResponse

from django.contrib.auth.decorators import login_required

from decimal import Decimal

from makerlab.courses.forms import AttendeeForm

from .models import Course,CourseDate,CourseSection,Attendee,WhatYoullLearn


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

    # get whatylls for this course
    whatylls = WhatYoullLearn.objects.filter(course=course)

    # get courseDates 
    courseDates = CourseDate.objects.filter(course=course).order_by('start_date')

    # get courseSections
    courseSections = CourseSection.objects.filter(course=course)

    return render(request, 'courses/detail.html',{'course':course, 'whatylls':whatylls, 'courseDates':courseDates, 'courseSections':courseSections})

def get_attendee(request, id):
    form = AttendeeForm()

    courseDate = None
    
    if request.POST:
        form = AttendeeForm(request.POST)

        if form.is_valid():

            try:
                courseDate = CourseDate.objects.get(pk=id)
            except:
                raise Http404("Not found.")
        
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            address = form.cleaned_data['address']

            try:
                attendee = Attendee.objects.get(email=email, courseDate=courseDate)
            except:
                attendee = None 
            
            if attendee:
                if attendee.paid:
                    # problem
                    return redirect('home')
                #redirect the user to payment moncash
                return redirect('enroll', attendee.id)
                
            attendee = Attendee.objects.create(first_name=first_name, last_name=last_name, email=email, telephone=telephone, address=address, courseDate=courseDate)

            #redirect the user to payment moncash
            return redirect('enroll', attendee.id)
    
    return render(request, 'courses/attendee.html', {'form':form, 'courseDate':courseDate})



def course_enrollement(request,id):

    try:
        attendee = Attendee.objects.get(pk=id)
    except:
        raise Http404('Not found error')
    
    courseDate = attendee.courseDate

    moncash2pay = round(float(courseDate.price)/0.98)
    moncash_fee = round(moncash2pay*0.02)+10
    total2pay = float(courseDate.price)+moncash_fee

    soldOut = False 
    paid = False 

    if attendee.paid:
        paid = True

    if courseDate.remainPlaces <= 0:
        soldOut=True

    return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'enrolled':paid,'soldOut':soldOut, 'total2pay':total2pay, 'moncash_fee':moncash_fee, 'attendee':attendee})

    

def search_results(request):
    q = request.GET.get('q','')

    courses =  Course.objects.annotate(search = SearchVector('title','description'))
    if courses ==  q :
        courses =courses.filter(title__contains=q)[:25]
    else:
        courses =courses.filter(title__icontains=q)[:25]
    return render(request, 'courses/search_results.html',{'courses':courses,'q':q})