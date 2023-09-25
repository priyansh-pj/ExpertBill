from django.db import models, transaction
from django.core.validators import RegexValidator


from store.models import *


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_organization = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.organization} - ({self.invoice_organization}) ({self.supplier})"

    @classmethod
    @transaction.atomic
    def create_invoice(cls, organization, supplier, total):
        try:
            invoice = cls.objects.create(
                organization=organization,
                supplier=supplier,
                total=float(total) if total.isdigit() else 0,
            )
            return invoice
        except Exception as e:
            print(f"Error creating invoice: {str(e)}")

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


class InvoicePayment(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    method = models.CharField(max_length=100, default="Cash")
    payment = models.IntegerField()

    @classmethod
    @transaction.atomic
    def insert_payment_method(cls, invoice, method, payment):
        try:
            cls.objects.create(
                invoice=invoice,
                method=method,
                payment=float(payment) if payment.isdigit() else 0,
            )
        except Exception as e:
            print(f"Error inserting payment: {str(e)}")


class InvoiceProduct(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @classmethod
    @transaction.atomic
    def register_invoice_product(
        cls, organization, invoice, product, gst, discount, sub_total
    ):
        try:
            cls.objects.create(
                organization=organization,
                invoice=invoice,
                product=product,
                gst=float(gst) if gst.isdigit() else 0,
                discount=float(discount) if discount.isdigit() else 0,
                sub_total=float(sub_total) if sub_total.isdigit() else 0,
            )
        except Exception as e:
            print(f"Error creating Invoice Product: {str(e)}")

    def __str__(self):
        return f"{self.organization} - ({self.invoice}) ({self.product})"
