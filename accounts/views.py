from django.shortcuts import render, redirect
from accounts.forms import SignUpUser
from django.contrib import messages
# Create your views here.
def signUpuser(request):
    if request.method == 'POST':
        form = SignUpUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been successful !')
    else:
        form = SignUpUser()
    return render(request, 'page/signup.html', {'form': form})