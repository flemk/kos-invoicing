from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("<int:project_id>/invoice", views.invoice, name="invoice"),
    path("<int:project_id>/invoice/create", views.invoice_create, name="invoice_create"),
    path("<int:project_id>/customer", views.customer, name="customer"),
    path("<int:project_id>/customer/create", views.customer_create, name="customer_create"),
    path("<int:project_id>/payee", views.payee, name="payee"),
    path("<int:project_id>/payee/create", views.payee_create, name="payee_create"),
]
