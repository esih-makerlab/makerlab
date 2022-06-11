from django.shortcuts import render, redirect 

from django.conf import settings 
from .models import CouponTransaction

from makerlab.courses.models import Course,CourseDate,Attendee

from django.contrib.auth.decorators import login_required

from django.utils.translation import gettext_lazy as _

from django.contrib import messages

from django.http import Http404,HttpResponse

from django_simple_coupons.validations import validate_coupon

from django_simple_coupons.models import Coupon


def course_payement(request):
    if request.method == 'POST':
        coupon_code=request.POST['coupon_code']
        attendee_id=request.POST['attendee_id']
        
        try:
            attendee = Attendee.objects.get(pk=attendee_id)
        except:
            raise Http404("Not found course date.")

        courseDate = attendee.courseDate

        validate = validate_coupon(coupon_code=coupon_code, user=attendee)
        
        if validate['valid']:

            coupon = Coupon.objects.get(code=coupon_code)

            new_price = coupon.get_discounted_value(courseDate.price)

            if new_price == 0:
                coupon.use_coupon(user=attendee)
                
                couponTransaction = CouponTransaction.objects.create(courseDate=courseDate,payor=attendee,status=CouponTransaction.Status.COMPLETE)

                attendee.paid = True
                attendee.save()

                return render(request, 'courses/payement.html',{'success':True,'attendee':attendee,'courseDate':courseDate})
            else:

                messages.error(request,_("valeur coupon insuffisante"))

                return render(request, 'courses/payement.html',{'success':False,'courseDate':courseDate})
        else:

            messages.error(request,validate['message'])

            return render(request, 'courses/payement.html',{'success':False,'courseDate':courseDate})
    else:
        return redirect('/home')