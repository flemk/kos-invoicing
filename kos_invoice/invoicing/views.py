from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Customer, Project, Payee
from .modules.translate_service import TranslateService
from .forms import CustomerForm, InvoiceForm, PayeeForm

ts = TranslateService()

def login_view(request):
    context = {
        'ts': ts,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not hasattr(user, 'userprofile') or user.userprofile.email_confirmed is False:
                return render(request, 'login.html',
                              context={'login_error':
                                       'Account not yet activated. Please check your inbox.'})

            login(request, user)
            return dashboard(request)
        else:
            print('Invalid credentials')
            return render(request, 'login.html', context={'login_error': 'Invalid credentials'})

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'login.html', context)

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
def invoice_create(request, project_id):
    user = request.user
    form = InvoiceForm()

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'templates/html/success.html', {'ts': ts})
        else:
            form = InvoiceForm(request.POST)

    context = {
        'ts': ts,
        'form_title': 'Create Invoice',
        'form': form,
    }
    return render(request, 'templates/html/form.html', context)

def customer(request, project_id):
    project = Project.objects.get(id=project_id)
    customers = Customer.objects.filter(project=project)

    context = {
        'ts': ts,
        'customers': customers,
        'project_id': str(project_id),
    }
    return render(request, 'templates/html/customer.html', context)

def customer_create(request, project_id):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('dashboard')
        form = CustomerForm(request.POST)

    context = {
        'ts': ts,
        'form_title': 'Create Customer',
        'form': form,
    }
    return render(request, 'templates/html/form.html', context)

def payee(request, project_id):
    project = Project.objects.get(id=project_id)
    payees = Payee.objects.filter(project=project)

    context = {
        'ts': ts,
        'project_id': str(project_id),
        'payees': payees,
    }
    return render(request, 'templates/html/payee.html', context)

def payee_create(request, project_id):
    form = PayeeForm()

    if request.method == 'POST':
        form = PayeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payee created successfully.')
            return redirect('dashboard')
        form = PayeeForm(request.POST)

    context = {
        'ts': ts,
        'form_title': 'Create Payee',
        'form': form,
    }
    return render(request, 'templates/html/form.html', context)
