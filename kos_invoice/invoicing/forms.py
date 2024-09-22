from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Project, Customer, Payee, Invoice, InvoiceItem

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username'}), label=False)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}), label=False)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), label=False)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}), label=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(), # TODO filter by user
        widget=forms.Select(
            attrs={'class': 'input', 'placeholder': 'Select Project'})
        )
    invoice_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Invoice Number'}))
    invoice_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date',}))
    due_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}))
    buyer_reference = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Buyer Reference'}))
    payee = forms.ModelChoiceField(
        queryset=Payee.objects.all(),
        widget=forms.Select(
            attrs={'class': 'input', 'placeholder': 'Select Payee'})) # TODO filter by project
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(
            attrs={'class': 'input', 'placeholder': 'Select Customer'})) # TODO filter by project
    payment_means_code = forms.ChoiceField(
        choices=[
            ('58', 'SEPA credit transfer'), # TODO read from json config file
        ],
        widget=forms.Select(
            attrs={'class': 'input', 'placeholder': 'Payment Means Code'}))
    payee_financial_account = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Payee Financial Account'}))
    payment_terms = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Payment Terms'}))
    tax_scheme = forms.ChoiceField(
        choices=[
            ('VAT', 'VAT'), # TODO read from json config file
        ],
        widget=forms.Select(
        attrs={'class': 'input', 'placeholder': 'Tax Scheme'}))
    price_tax = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Price Tax'}))
    price_net = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Price Net'}))
    price_full = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Price Full'}))
    tax_percentage = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Tax Percentage'}))
    note = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input', 'style': 'height: 5rem;', 'placeholder': 'Note'}))

    class Meta:
        model = Invoice
        fields = [
            'project',
            'invoice_number',
            'invoice_date',
            'due_date',
            'buyer_reference',
            'payee',
            'customer',
            'payment_means_code',
            'payee_financial_account',
            'payment_terms',
            'tax_scheme',
            'price_tax',
            'price_net',
            'price_full',
            'tax_percentage',
            'note',
            ]

class InvoiceItemForm(forms.ModelForm):
    period_start = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date',}))
    period_end = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date',}))
    class Meta:
        model = InvoiceItem
        fields = '__all__'
