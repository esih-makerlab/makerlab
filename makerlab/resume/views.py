from django.shortcuts import render
from django.http import Http404
from .models import Resume


# def get_resume(request,id):
#     resume=None
#     try:
#         resume = Resume.objects.get(user__id=id)
#     except Resume.DoesNotExist:
#         raise Http404("Not found.")

#     return render(request, 'resume/get.html',{'resume':resume})
