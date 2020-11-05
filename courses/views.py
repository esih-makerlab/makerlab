from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

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

def course_details(request):
    return render(request, 'courses/detail.html')

def course_enrollement(request):
    return render(request, 'courses/enrollement.html')

def course_payement(request):
    return render(request, 'courses/payement.html')

def search_results(request):
    q = request.GET.get('q')

    filter_search = request.GET.get('filter')

    if not filter_search:
        filter_search = 'course'

    if filter_search == 'teacher':
        teachers = [

        ]
    else:


        courses = [
            {'title':'intro C++','description':'C++ est un langage de programmation compilé permettant la programmation sous de multiples paradigmes. Ses bonnes performances, et sa compatibilité avec le C en font un des langages de programmation les plus utilisés dans les applications où la performance est critique.'},
            {'title':'intro C++','description':'C++ est un langage de programmation compilé permettant la programmation sous de multiples paradigmes. Ses bonnes performances, et sa compatibilité avec le C en font un des langages de programmation les plus utilisés dans les applications où la performance est critique.'},
            {'title':'intro C++','description':'C++ est un langage de programmation compilé permettant la programmation sous de multiples paradigmes. Ses bonnes performances, et sa compatibilité avec le C en font un des langages de programmation les plus utilisés dans les applications où la performance est critique.'},
            {'title':'intro C++','description':'C++ est un langage de programmation compilé permettant la programmation sous de multiples paradigmes. Ses bonnes performances, et sa compatibilité avec le C en font un des langages de programmation les plus utilisés dans les applications où la performance est critique.'}
        ]

    return render(request, 'courses/search_results.html',{'courses':courses,'teachers':teachers,'filter':filter_search})