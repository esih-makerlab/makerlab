from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model
from django.http import Http404

from django.contrib.auth.decorators import login_required

from django.conf import settings

from moncash.models import CourseTransaction

import moncashify

from .models import Course,CourseDate,Attendee

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

@login_required(login_url='/account/login')
def course_enrollement(request,id):

    try:
        courseDate = CourseDate.objects.get(pk=id)
    except CourseDate.DoesNotExist:
        raise Http404("Not found.")

    if courseDate.remainPlaces() <= 0:
        return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'soldOut':True})

    return render(request, 'courses/enrollement.html',{'courseDate':courseDate,'soldOut':False})

@login_required(login_url='/account/login')
def course_payement(request):
    transactionId = request.GET.get('transactionId',None)

    if transactionId:
        moncash = moncashify.API(settings.MONCASH['CLIENT_ID'], settings.MONCASH['SECRET_KEY'], True)
        transaction = moncash.transaction_details_by_transaction_id(transaction_id=transactionId)
        
        if transaction:
            try:
                courseTransaction = CourseTransaction.objects.get(pk=transaction["payment"]["reference"])
            except CourseDate.DoesNotExist:
                raise Http404("Not found.")

            courseTransaction.status = CourseTransaction.Status.COMPLETE
            courseTransaction.save()

            attendee = Attendee.objects.create(date=courseTransaction.courseDate,attendee=request.user)

            return render(request, 'courses/payement.html',{'success':True,'attendee':attendee})
        else:
            return render(request, 'courses/payement.html',{'success':False})
    else:
        return render(request, 'courses/payement.html',{'success':False})
    
    

def search_results(request):
    q = request.GET.get('q','')

    courses =  Course.objects.annotate(search = SearchVector('title','description')).filter(search__icontains=q)[:25]

    return render(request, 'courses/search_results.html',{'courses':courses,'q':q})