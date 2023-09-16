from django.db import models
from django.core.validators import RegexValidator


from store.models import *


# Create your models here.
from django.db import models
from decimal import Decimal


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_organization = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    method = models.CharField(max_length=100, default="Cash")
    method_payment = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"{self.organization} - ({self.invoice_organization}) ({self.supplier})"

    def save(self, *args, **kwargs):
        existing_invoices = Invoice.objects.filter(organization=self.organization)

        if existing_invoices.exists():
            highest_id = existing_invoices.aggregate(
                models.Max("invoice_organization")
            )["invoice_organization__max"]
            if highest_id is not None:
                self.invoice_organization = highest_id + 1
            else:
                self.invoice_organization = 1
        else:
            self.invoice_organization = 1

        super().save(*args, **kwargs)


class InvoiceProduct(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.organization} - ({self.invoice}) ({self.product})"
