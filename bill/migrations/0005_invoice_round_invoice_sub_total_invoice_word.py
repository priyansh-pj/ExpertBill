# Generated by Django 4.2.8 on 2024-01-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0004_invoiceproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='round',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='invoice',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='invoice',
            name='word',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
