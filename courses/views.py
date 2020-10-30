from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from .models import Course , CourseDate
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.postgres.search import SearchVector
from .forms import SearchFrom

def home(request):
        
    page = request.GET.get('page', 1)
        
    paginator = Paginator(Course.objects.all(), 3)

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    form_class= SearchFrom

    return render(request, 'courses/home.html',{'courses':courses})           

def course_details(request):
    return render(request, 'courses/detail.html')

def course_enrollement(request):
    return render(request, 'courses/enrollement.html')

def course_payement(request):
    return render(request, 'courses/payement.html')



class SearchResultsView(ListView):

    template_name = 'courses/course_list.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')      
        object_list =  Course.objects.annotate(search = SearchVector('title')).filter(search__icontains=query)
        info = CourseDate.objects.annotate(search = SearchVector('course'))
        
        if object_list:
            return object_list
        
        if info:
            return info
           
        
        
         
        
            

    

