# Generated by Django 5.0.7 on 2024-09-21 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_invoiceposition_supplier_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvoicePosition',
            new_name='InvoiceItem',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='invoice_positions',
            new_name='invoice_items',
        ),
    ]
