# Generated by Django 5.0.7 on 2024-09-21 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0005_rename_supplier_payee_rename_supplier_invoice_payee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_items',
        ),
    ]
