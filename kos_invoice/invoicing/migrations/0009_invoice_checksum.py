# Generated by Django 5.0.7 on 2024-09-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0008_rename_customer_invoice_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='checksum',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
