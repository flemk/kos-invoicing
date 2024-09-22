from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),

    path("<int:project_id>/invoice", views.invoice, name="invoice"),
    path("<int:project_id>/invoice/<int:invoice_id>", views.invoice_detail, name="invoice_detail"),
    path("<int:project_id>/invoice/<int:invoice_id>/edit", views.invoice_edit, name="invoice_edit"),
    path("<int:project_id>/invoice/create", views.invoice_create, name="invoice_create"),

    path("<int:project_id>/invoice/<int:invoice_id>/item/add", views.invoice_item_add, name="invoice_item_add"),

    path("<int:project_id>/customer", views.customer, name="customer"),
    path("<int:project_id>/customer/<int:customer_id>", views.customer_detail,
         name="customer_detail"),
    path("<int:project_id>/customer/<int:customer_id>/edit", views.customer_edit,
         name="customer_edit"),
    path("<int:project_id>/customer/create", views.customer_create, name="customer_create"),

    path("<int:project_id>/payee", views.payee, name="payee"),
    path("<int:project_id>/payee/<int:payee_id>", views.payee_detail, name="payee_detail"),
    path("<int:project_id>/payee/<int:payee_id>/edit", views.payee_edit, name="payee_edit"),
    path("<int:project_id>/payee/create", views.payee_create, name="payee_create"),
]
