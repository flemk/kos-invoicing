import secrets
from django.db import models
from django.contrib.auth.models import User

def generate_api_key(): return secrets.token_hex(50)

class UserProfile(models.Model):
    # email is handled by User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    email_confirmed = models.BooleanField(default=False)
    user_hash = models.CharField(max_length=100, blank=True, default=generate_api_key)
    projects = models.ManyToManyField('Project', blank=True)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)

class Customer(models.Model):
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=False)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)

    # Required by xml template
    customer_id = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False) # TODO change to Choice "DE" etc
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return str(self.name)

class Supplier(models.Model):
    # Required by xml template
    email = models.EmailField(max_length=100, blank=False)
    company_name = models.CharField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False) # TODO change to Choice "DE" etc
    company_id = models.CharField(max_length=100, blank=False)
    hra_no = models.CharField(max_length=100, blank=False)
    hra_name = models.CharField(max_length=100, blank=False)
    contact_name = models.CharField(max_length=100, blank=False)
    contact_phone = models.CharField(max_length=100, blank=False)
    contact_email = models.EmailField(max_length=100, blank=False)

class Invoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    # Required by xml template
    invoice_number = models.CharField(max_length=100, blank=False)
    invoice_date = models.DateField(blank=False)
    due_date = models.DateField(blank=False)
    note = models.TextField(blank=True)
    buyer_reference = models.CharField(max_length=100, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    Customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment_means_code = models.CharField(max_length=100, blank=False) # TODO change to Choice "58" -> IBAN etc
    payee_financial_account = models.CharField(max_length=100, blank=False)
    payment_terms = models.CharField(max_length=100, blank=False)

    tax_scheme = models.CharField(max_length=100, blank=False) # TODO change to Choice "VAT" etc
    price_tax = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    price_full = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

class InvoicePosition(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    # Required by xml template
    name = models.CharField(max_length=100, blank=False)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField(blank=False)
    period_end = models.DateField(blank=False)
