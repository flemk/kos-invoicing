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
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    # Required by xml template
    name = models.CharField(max_length=100, blank=False)
    customer_id = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=2,
                           blank=False,
                            choices=[
                               ("DE", "Germany"),
                           ]) # TODO read from json config file

    def __str__(self):
        return str(self.name)

class Payee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    # Required by xml template
    email = models.EmailField(max_length=100, blank=False)
    company_name = models.CharField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=2,
                               blank=False,
                               choices=[
                                   ("DE", "Germany"),
                               ]) # TODO read from json config file
    company_id = models.CharField(max_length=100, blank=False)
    hra_no = models.CharField(max_length=100, blank=False)
    contact_name = models.CharField(max_length=100, blank=False)
    contact_phone = models.CharField(max_length=100, blank=False)
    contact_email = models.EmailField(max_length=100, blank=False)

    def __str__(self):
        return str(self.company_name)

class Invoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    # Required by xml template but for now static
    invoice_type_code = 380
    currency_code = "EUR"
    tax_category_code = "S"

    # Required by xml template
    invoice_number = models.CharField(max_length=100, blank=False)
    invoice_date = models.DateField(blank=False)
    due_date = models.DateField(blank=False)
    note = models.TextField(blank=True)
    buyer_reference = models.CharField(max_length=100, blank=True)

    payee = models.ForeignKey(Payee, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    payment_means_code = models.CharField(max_length=3,
                                          blank=False,
                                          choices=[
                                              ("58", "SEPA")]) # TODO read from json config file
    payee_financial_account = models.CharField(max_length=100, blank=False)
    payment_terms = models.CharField(max_length=100, blank=False)

    tax_scheme = models.CharField(max_length=100,
                                  blank=False,
                                  choices=[
                                      ("VAT", "VAT"),
                                      ]) # TODO read from json config file
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def price_net(self):
        return sum([item.price_net for item in self.invoice_items.all()])

    def price_gross(self):
        return self.price_net() * (1 + self.tax_percentage / 100)

    def __str__(self):
        return str(self.invoice_number)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice,
                                on_delete=models.CASCADE,
                                related_name='invoice_items')
    
    # Required by xml template but for now static
    unit_code = "XPP"

    # Required by xml template
    name = models.CharField(max_length=100, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField(blank=False)
    period_end = models.DateField(blank=False)
