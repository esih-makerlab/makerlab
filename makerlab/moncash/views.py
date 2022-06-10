from django.shortcuts import render, redirect 

from django.conf import settings 
from .models import CourseTransaction

from makerlab.courses.models import Course,CourseDate,Attendee

from django.contrib import messages

from django.http import Http404,HttpResponse,HttpResponseRedirect

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.urls import reverse

import moncash

gateway = moncash.Moncash(
        client_id=settings.MONCASH['CLIENT_ID'],
        client_secret=settings.MONCASH['SECRET_KEY'],
        environment=moncash.environment.Sandbox
    )


@login_required(login_url='/account/login')
def CourseProceed(request,id):
    try:
        courseDate = CourseDate.objects.get(pk=id)
    except CourseDate.DoesNotExist:
        raise Http404("Not found.")

    try:
        courseTransaction = CourseTransaction.objects.get(courseDate=courseDate,payor=request.user)
    except:
        courseTransaction = None
    
    moncash2pay = round(float(courseDate.price)/0.98)
    moncash_fee = round(moncash2pay*0.02)+10
    total2pay = float(courseDate.price)+moncash_fee

    if not courseTransaction:

        courseTransaction = CourseTransaction.objects.create(courseDate=courseDate,payor=request.user)
        
        try:
            get_paid_url = gateway.payment.create(amount=total2pay, reference=courseTransaction.id)
        except moncash.exceptions.MoncashError:
            raise HttpResponse(_("Erreur Moncash, reesseyer"))

        return redirect(get_paid_url)
  
    if courseTransaction.status == 'PENDING':

        try:
            get_paid_url = gateway.payment.create(amount=total2pay, reference=courseTransaction.id)
        except moncash.exceptions.MoncashError:
            raise HttpResponse(_("Erreur Moncash, reesseyer"))

        return redirect(get_paid_url)
    
    else:
        try:
            attendee = Attendee.objects.get(start_date=courseTransaction.courseDate, attendee=request.user)
        except:
            raise Http404("Not found.")
       
        return render(request, 'courses/payement.html',{'success':True,'attendee':attendee,'courseDate':courseTransaction.courseDate})



@login_required(login_url='/account/login')
def course_payement(request):
    transactionId = request.GET.get('transactionId',None)

    if transactionId:
        try:
            transaction = gateway.payment.get_by_id(transactionId=transactionId)
        except:
            transaction = None
        
        if transaction:
            try:
                courseTransaction = CourseTransaction.objects.get(pk=transaction["reference"])
            except CourseTransaction.DoesNotExist:
                raise Http404("Not found.")

            courseTransaction.status = CourseTransaction.Status.COMPLETE
            courseTransaction.save()

            try:
                attendee = Attendee.objects.get(start_date=courseTransaction.courseDate, attendee=request.user)
            except:
                attendee = None

            if not attendee:
                attendee = Attendee.objects.create(start_date=courseTransaction.courseDate,attendee=request.user)

            return render(request, 'courses/payement.html',{'success':True,'attendee':attendee,'courseDate':courseTransaction.courseDate})
        else:
            messages.error(request,_("Erreur Moncash, reesseyer"))

            return render(request, 'courses/payement.html',{'success':False,'courseDate':courseTransaction.courseDate})
    else:
        return render(request, 'courses/payement.html',{'success':False,})