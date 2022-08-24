from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect

from django.conf import settings
from django.utils import translation


def index(request):
    return redirect('/home')

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

# Error Views ...
def error403(request, exception=None):
    return render(request, '403.html', status=403) 

def error404(request, exception=None):
    return render(request, '404.html', status=404)

def error500(request):
    return render(request, '500.html', status=500)


def dashboard(request):
    return render(request, 'pages/dashboard.html')                

def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response