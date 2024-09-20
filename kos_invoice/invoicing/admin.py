from django.contrib import admin
from .models import UserProfile, Project, Customer

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname')
admin.site.register(UserProfile, UserProfileAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
admin.site.register(Project, ProjectAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'city', 'country', 'project')
admin.site.register(Customer, CustomerAdmin)
