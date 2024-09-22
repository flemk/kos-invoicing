from django.contrib import admin
from .models import UserProfile, Project, Customer, Payee, Invoice, InvoiceItem

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
admin.site.register(UserProfile, UserProfileAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
admin.site.register(Project, ProjectAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'city', 'country', 'project')
admin.site.register(Customer, CustomerAdmin)

class PayeeAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'city', 'country')
admin.site.register(Payee, PayeeAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'payee')
admin.site.register(Invoice, InvoiceAdmin)

class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'name')
admin.site.register(InvoiceItem, InvoiceItemAdmin)