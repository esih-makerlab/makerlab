from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Courses


def home(request):
    price = request.GET.get('price', 0)
    currency = request.GET.get('currency', 'HTG')
    date = request.GET.get('date', timezone.now())
    tag = request.GET.get('tag', None)
    
    if not date:
        date = timezone.now()
        
    page = request.GET.get('page', 1)

    if tag is not None:
        try:
            courses = Courses.objects.filter(price__gte=price,currency=currency,date__gte=date,tags__contains=[tag]).order_by('date')
        except Courses.DoesNotExist:
            courses= None
    else:
        try:
            courses= Courses.objects.filter(price__gte=price,currency=currency,date__gte=date).order_by('date')
        except Courses.DoesNotExist:
            courses= None
        
    

    if courses is not None:
        paginator = Paginator(courses, 1)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

    return render(request, 'courses/home.html',{'courses':courses})           
