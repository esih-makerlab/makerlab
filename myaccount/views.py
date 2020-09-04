from django.shortcuts import render
from myaccount.forms import SignUpUser

# Create your views here.


def signUpUser(request):
    form = SignUpUser()
    return render(request, 'page/signup.html', {'form': form})