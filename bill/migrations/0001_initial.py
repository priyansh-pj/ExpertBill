# Generated by Django 5.0.1 on 2024-01-14 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_organization', models.IntegerField()),
                ('date', models.DateField()),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('round', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('word', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoicePayment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(default='Cash', max_length=100)),
                ('payment', models.IntegerField()),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('gst', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
