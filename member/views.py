from django.shortcuts import render

from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST) 
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # set the chosinfg password 
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    
    return render(
        request, 
        'account/register.html',
        {'user_form': user_form}
    )

def user_login(request):
    
        
            # user = authenticate(
            #     request,
            #     username=cd['username'],
            #     password=cd['password']
            # )
            # if user is not None:
            #     if user.is_active:
            #         login(request, user)
            #         return HttpResponse('Authenticated successfully')
            #     else:
            #         return HttpResponse('Disable account')
            # else:
            #     return HttpResponse('Invalid account')

    return render(request, 'account/login.html')