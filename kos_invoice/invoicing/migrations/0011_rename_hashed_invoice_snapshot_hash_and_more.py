# Generated by Django 5.0.7 on 2024-09-24 19:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0010_rename_checksum_invoice_hashed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='hashed',
            new_name='snapshot_hash',
        ),
        migrations.AddField(
            model_name='invoice',
            name='snapshot_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]