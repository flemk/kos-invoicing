from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("project/invoice/create", views.invoice_create, name="invoice_create"),
]
