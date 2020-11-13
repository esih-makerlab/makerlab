from django.shortcuts import render, redirect 

from django.conf import settings 
from .models import CourseTransaction
from courses.models import CourseDate

from django.contrib.auth.decorators import login_required

import moncashify

@login_required(login_url='/account/login')
def CourseProceed(request,id):
    moncash = moncashify.API(settings.MONCASH['CLIENT_ID'], settings.MONCASH['SECRET_KEY'], True)

    try:
        courseDate = CourseDate.objects.get(pk=id)
    except CourseDate.DoesNotExist:
        raise Http404("Not found.")

    courseTransaction = CourseTransaction.objects.create(courseDate=courseDate,payor=request.user)

    payment = moncash.payment(order_id=courseTransaction.id, amount=int(courseDate.price))

    url = payment.redirect_url 

    return redirect(url)


