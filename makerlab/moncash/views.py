from django.shortcuts import render, redirect 

from django.conf import settings 
from .models import CourseTransaction

from makerlab.courses.models import Course,CourseDate,Attendee

from django.contrib import messages

from django.http import Http404,HttpResponse

from django.utils.translation import gettext_lazy as _

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

    try:
        payment = moncash.payment(order_id=courseTransaction.id, amount=int(courseDate.price))
    except:
        raise HttpResponse(_("Erreur Moncash, reesseyer"))

    url = payment.redirect_url 

    return redirect(url)


@login_required(login_url='/account/login')
def course_payement(request):
    transactionId = request.GET.get('transactionId',None)

    if transactionId:
        moncash = moncashify.API(settings.MONCASH['CLIENT_ID'], settings.MONCASH['SECRET_KEY'], True)
        try:
            transaction = moncash.transaction_details_by_transaction_id(transaction_id=transactionId)
        except:
            transaction = None
        
        if transaction:
            try:
                courseTransaction = CourseTransaction.objects.get(pk=transaction["payment"]["reference"])
            except CourseTransaction.DoesNotExist:
                raise Http404("Not found.")

            courseTransaction.status = CourseTransaction.Status.COMPLETE
            courseTransaction.save()

            attendee = Attendee.objects.create(date=courseTransaction.courseDate,attendee=request.user)

            return render(request, 'courses/payement.html',{'success':True,'attendee':attendee,'courseDate':courseTransaction.courseDate})
        else:
            messages.error(request,_("Erreur Moncash, reesseyer"))

            return render(request, 'courses/payement.html',{'success':False,'courseDate':courseTransaction.courseDate})
    else:
        return render(request, 'courses/payement.html',{'success':False,'courseDate':courseTransaction.courseDate})