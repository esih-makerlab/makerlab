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


@login_required(login_url='/account/login')
def course_payement(request):
    if request.method == 'POST':
        coupon_code=request.POST['coupon_code']
        courseDate_id=request.POST['courseDate_id']
        
        try:
            courseDate = CourseDate.objects.get(pk=courseDate_id)
        except CourseDate.DoesNotExist:
            raise Http404("Not found course date.")

        validate = validate_coupon(coupon_code=coupon_code, user=request.user)
        
        if validate['valid']:

            coupon = Coupon.objects.get(code=coupon_code)

            new_price = coupon.get_discounted_value(courseDate.price)

            if new_price == 0:
                coupon.use_coupon(user=request.user)
                
                couponTransaction = CouponTransaction.objects.create(courseDate=courseDate,payor=request.user,status=CouponTransaction.Status.COMPLETE)

                attendee = Attendee.objects.create(start_date=couponTransaction.courseDate,attendee=request.user)

                return render(request, 'courses/payement.html',{'success':True,'attendee':attendee,'courseDate':courseDate})
            else:

                messages.error(request,_("valeur coupon insuffisante"))

                return render(request, 'courses/payement.html',{'success':False,'courseDate':courseDate})
        else:

            messages.error(request,validate['message'])

            return render(request, 'courses/payement.html',{'success':False,'courseDate':courseDate})
    else:
        return redirect('/home')