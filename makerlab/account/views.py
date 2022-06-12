from django.shortcuts import render,redirect
from .forms import AddUserForm,LoginForm,UpdateProfileForm,ChangePasswordForm,ResetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate, login, logout,REDIRECT_FIELD_NAME
from .models import User


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMultiAlternatives

from django.contrib import messages

from django.forms.models import model_to_dict

from makerlab.courses.models import CourseDate

@login_required(login_url='/account/login')
def verify_email_request(request):

    user = request.user
    
    message = render_to_string('account/emails/verification.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })     

    msg = EmailMultiAlternatives(
        subject = _('Comfirm your email'),
        to=[user.email])

    msg.attach_alternative(message, "text/html")

    msg.tags = ["activation", "verification","information","contact","confirmed"]
    msg.track_clicks = True

    msg.send()

    messages.warning(request,_('Please Confirm your email to complete registration.'))

    next_url = request.GET.get(REDIRECT_FIELD_NAME)
                
    if next_url :
        return redirect(next_url)
    else:
        return redirect('/account/profile')

def login_user(request):
    if request.method == 'POST':
        
        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request,username=email, password=password)

            if user is not None:
                login(request, user)

                next_url = request.GET.get(REDIRECT_FIELD_NAME)
                
                if next_url :
                    return redirect(next_url)
                return redirect('/account/profile')
        else:
            return render(request,'account/login.html',{'form':form})

    else:
        return render(request,'account/login.html',{'form':LoginForm(None)})

def register_user(request):
    if request.method == 'POST':

        form = AddUserForm(request.POST)

        if form.is_valid(): 

            form.save(commit = True)  

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = authenticate(request,username=email, password=password)

            login(request, user)

            next_url = request.GET.get(REDIRECT_FIELD_NAME)
            
            if next_url :
                return redirect(next_url)
            return redirect('/account/profile')

        else:
		
            return render(request,'account/register.html',{'form':form,'submit':_('submit')})
    else:
        return render(request,'account/register.html',{'form':AddUserForm(None),'submit':_('submit')})

def logout_user(request):
    logout(request)
    return redirect('/')

def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()

        login(request, user)
        

        message = render_to_string('account/emails/welcome.html', {
            'user': user,
            'domain': get_current_site(request).domain
        })     

        msg = EmailMultiAlternatives(
            subject = _('Welcome'),
            to=[user.email])

        msg.attach_alternative(message, "text/html")

        msg.tags = ["welcome", "information","contact","confirmed"]
        msg.track_clicks = True

        msg.send()

        messages.success(request,_('Your email have been confirmed.'))

        return redirect('/account/profile')

    else:

        messages.error(request,_('The confirmation link was invalid.'))
        
        return redirect('/account/login')

def reset_password_request(request):

    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:

            message = render_to_string('account/emails/reset_password.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })  

            msg = EmailMultiAlternatives(
                subject = _('Reset Your Password'),
                to=[user.email])

            msg.attach_alternative(message, "text/html")

            msg.tags = ["reset", "password","information","contact","confirmed"]
            msg.track_clicks = True

            msg.send()

            messages.warning(request,_('Please complete your password reset by clicking on the link in your email.'))

            next_url = request.GET.get(REDIRECT_FIELD_NAME)
                    
            if next_url :
                return redirect(next_url)
            else:
                return redirect('/account/login')
        else:
            messages.error(request,_('There is no user asssociate with this email.'))

            return render(request,'account/reset_password.html',{'form':LoginForm(None)})
    return render(request,'account/reset_password.html',{'form':LoginForm(None)})
        
def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':

            form = ResetPasswordForm(request.POST,instance=user)
        
            if form.is_valid():
                login(request,form.save(commit=True))
                return redirect('/account/profile')
            else:
                return render(request,'account/reset_password_form.html',{'form':form})
            
        else:
            return render(request,'account/reset_password_form.html',{'form':ResetPasswordForm(None)})

    else:

        messages.error(request,_('The confirmation link was invalid.'))
        
        return redirect('/account/login')

@login_required(login_url='/account/login')
def change_password(request):
    user = request.user

    if request.method == 'POST':

        form = ChangePasswordForm(request.POST,instance=user)
        
        if form.is_valid():
            login(request,form.save(commit=True))
            return redirect('/account/profile')
        else:
            return render(request,'account/change_password.html',{'form':form})
        
    else:
        return render(request,'account/change_password.html',{'form':ChangePasswordForm(None)})

@login_required(login_url='/account/login')
def edit_profile(request):

    user = request.user

    if request.method == 'POST':
        
        form = UpdateProfileForm(request.POST, request.FILES,instance=user)
    
        if form.is_valid():
            login(request,form.save(commit=True))
            return redirect('/account/profile')
        else:
            return render(request,'account/edit_profile.html',{'form':form})
    else:
        initial_user = model_to_dict(user, fields=[field.name for field in user._meta.fields])
        initial_user['password'] = None
        
        return render(request,'account/edit_profile.html',{'form':UpdateProfileForm(initial=initial_user)})

@login_required(login_url='/account/login')
def profile(request):
    page = request.GET.get('page', 1)
        
    #paginator = Paginator(CourseDate.objects.filter(attendees=request.user).order_by('start_date'), 3)
    courseDates=None
    # try:
    #     courseDates = paginator.page(page)
    # except PageNotAnInteger:
    #     courseDates = paginator.page(1)
    # except EmptyPage:
    #     courseDates = paginator.page(paginator.num_pages)
    
    return render(request,'account/profile.html',{'courseDates':courseDates})