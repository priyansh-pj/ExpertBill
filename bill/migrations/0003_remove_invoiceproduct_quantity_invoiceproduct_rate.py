# Generated by Django 4.2.8 on 2024-01-08 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceproduct',
            name='quantity',
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
