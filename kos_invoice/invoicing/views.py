from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer, Invoice, InvoiceItem, Project, Payee
from .modules.translate_service import TranslateService
from .forms import CustomerForm, InvoiceForm, InvoiceItemForm, PayeeForm

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
        context['login_error'] = 'Invalid credentials'

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'templates/html/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

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
def invoice(request, project_id):
    project = Project.objects.get(id=project_id)
    invoices = Invoice.objects.filter(project=project)

    context = {
        'ts': ts,
        'invoices': invoices,
        'project': project,
    }
    return render(request, 'templates/html/invoice.html', context)

@login_required
def invoice_detail(request, project_id, invoice_id):
    project = Project.objects.get(id=project_id)
    invoice = Invoice.objects.get(id=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        'ts': ts,
        'project': project,
        'invoice': invoice,
        'items': items,
    }
    return render(request, 'templates/html/invoice_detail.html', context)

@login_required
def invoice_edit(request, project_id, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    form = InvoiceForm(instance=invoice)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('invoice_detail', project_id=project_id, invoice_id=invoice.id)
        form = InvoiceForm(request.POST, instance=invoice)

    context = {
        'ts': ts,
        'form_title': 'Edit Invoice',
        'form': form,
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
def invoice_create(request, project_id):
    user = request.user
    form = InvoiceForm()

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoice_detail', project_id=project_id, invoice_id=invoice.id)
        else:
            form = InvoiceForm(request.POST)

    context = {
        'ts': ts,
        'form_title': 'Create Invoice',
        'form': form,
        'complete_hint': 'Invoice Items can be added after completing this first step.',
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
def invoice_delete(request, project_id, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice.delete()
    messages.success(request, 'Invoice removed successfully.')
    return redirect('invoice', project_id=project_id)

@login_required
def invoice_export(request, project_id, invoice_id, filetype):
    invoice = Invoice.objects.get(id=invoice_id)
    items = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        'ts': ts,
        'invoice': invoice,
        'items': items,
    }
    return render(request, 'templates/xml/invoice.xml', context, content_type='text/xml')

@login_required
def invoice_item_add(request, project_id, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    form = InvoiceItemForm()

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice Item added successfully.')
            return redirect('invoice_detail', project_id=project_id, invoice_id=invoice.id)
        else:
            form = InvoiceItemForm(request.POST)

    context = {
        'ts': ts,
        'form_title': 'Add Invoice Item',
        'form': form,
        'complete_hint': 'You will be redirected to the Invoice after adding the item.',
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
def invoice_item_remove(request, project_id, invoice_id, item_id):
    item = InvoiceItem.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Invoice Item removed successfully.')
    return redirect('invoice_detail', project_id=project_id, invoice_id=invoice_id)

@login_required
def invoice_item_edit(request, project_id, invoice_id, item_id):
    item = InvoiceItem.objects.get(id=item_id)
    form = InvoiceItemForm(instance=item)

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice Item updated successfully.')
            return redirect('invoice_detail', project_id=project_id, invoice_id=invoice_id)
        form = InvoiceItemForm(request.POST, instance=item)

    context = {
        'ts': ts,
        'form_title': 'Edit Invoice Item',
        'form': form,
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
def customer(request, project_id):
    project = Project.objects.get(id=project_id)
    customers = Customer.objects.filter(project=project)

    context = {
        'ts': ts,
        'customers': customers,
        'project': project,
    }
    return render(request, 'templates/html/customer.html', context)

@login_required
def customer_detail(request, project_id, customer_id):
    return 0
    customer = Customer.objects.get(id=customer_id)

    context = {
        'ts': ts,
        'customer': customer,
    }
    return render(request, 'templates/html/customer_detail.html', context)

@login_required
def customer_edit(request, project_id, customer_id):
    customer = Customer.objects.get(id=customer_id)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer', project_id=project_id)
        form = CustomerForm(request.POST, instance=customer)

    context = {
        'ts': ts,
        'form_title': 'Edit Customer',
        'form': form,
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
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
    return render(request, 'templates/html_components/form.html', context)

@login_required
def payee(request, project_id):
    project = Project.objects.get(id=project_id)
    payees = Payee.objects.filter(project=project)

    context = {
        'ts': ts,
        'project': project,
        'payees': payees,
    }
    return render(request, 'templates/html/payee.html', context)

@login_required
def payee_detail(request, project_id, payee_id):
    return 0
    payee = Payee.objects.get(id=payee_id)

    context = {
        'ts': ts,
        'payee': payee,
    }
    return render(request, 'templates/html/payee_detail.html', context)

@login_required
def payee_edit(request, project_id, payee_id):
    payee = Payee.objects.get(id=payee_id)
    form = PayeeForm(instance=payee)

    if request.method == 'POST':
        form = PayeeForm(request.POST, instance=payee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payee updated successfully.')
            return redirect('payee', project_id=project_id)
        form = PayeeForm(request.POST, instance=payee)

    context = {
        'ts': ts,
        'form_title': 'Edit Payee',
        'form': form,
    }
    return render(request, 'templates/html_components/form.html', context)

@login_required
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
    return render(request, 'templates/html_components/form.html', context)

@login_required
def confirm(request):
    if request.method == 'POST':
        redirect_url_confirmed = request.POST.get('redirect_url_confirmed')
        redirect_url_declined = request.POST.get('redirect_url_declined')
        title = request.POST.get('title')
        message = request.POST.get('message')

        context = {
            'ts': ts,
            'redirect_url_confirmed': redirect_url_confirmed,
            'redirect_url_declined': redirect_url_declined,
            'title': title,
            'message': message,
        }
        return render(request, 'templates/html_components/confirm.html', context)
    return HttpResponseBadRequest()
