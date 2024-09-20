from django.shortcuts import render
from .modules.translate_service import TranslateService
from django.contrib.auth.decorators import login_required

ts = TranslateService()

def login(request):
    context = {
        'ts': ts,
    }
    return render(request, 'templates/html/login.html', context)

@login_required
def dashboard(request):
    user = request.user
    projects = user.userprofile.projects.all()

    context = {
        'ts': ts,
        'projects': projects,
    }
    return render(request, 'templates/html/dashboard.html', context)
