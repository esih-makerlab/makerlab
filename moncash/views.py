from django.shortcuts import render, redirect 

from django.conf import settings 

import moncashify

def proceed(request):
    order_id = 30
    amount = 1000 # HTG

    moncash = moncashify.API(settings.MONCASH['CLIENT_ID'], settings.MONCASH['SECRET_KEY'], True)

    payment = moncash.payment(order_id, amount)

    url = payment.redirect_url 

    return redirect(url)


