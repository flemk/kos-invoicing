from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("<int:project_id>/invoice/create", views.invoice_create, name="invoice_create"),
    path("<int:project_id>/customer", views.customer, name="customer"),
    path("<int:project_id>/customer/create", views.customer_create, name="customer_create"),
    path("<int:project_id>/supplier", views.supplier, name="supplier"),
    path("<int:project_id>/supplier/create", views.supplier_create, name="supplier_create"),
]
