from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .modules.translate_service import TranslateService
from .forms import InvoiceForm

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

@login_required
def invoice_create(request):
    user = request.user
    form = InvoiceForm()

    context = {
        'ts': ts,
        'form_title': 'Create Invoice',
        'form': form,
    }
    return render(request, 'templates/html/form.html', context)
