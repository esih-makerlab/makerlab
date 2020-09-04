from django.shortcuts import render
from django.views.decorators.http import require_POST
from myaccount.forms import SignUpUser

# Create your views here.
@require_POST
def user_login(request):
    data = {
        'username': request.POST.get('login_user'),
        'password': request.POST.get('login_pass')
    }
    if data['username'] and data['password']:
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('account:dashboard'))
                #return HttpResponse('Authentificated successfully')



def signUpUser(request):
    form = SignUpUser()
    return render(request, 'page/signup.html', {'signupform': form})