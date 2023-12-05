# Generated by Django 4.2.2 on 2023-11-16 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("organization", "0001_initial"),
        ("store", "0001_initial"),
        ("bill", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoiceproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.product"
            ),
        ),
        migrations.AddField(
            model_name="invoicepayment",
            name="invoice",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="bill.invoice"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="organization.organization",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.supplier"
            ),
        ),
    ]
