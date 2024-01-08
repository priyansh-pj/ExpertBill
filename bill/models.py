from django.db import models, transaction


from store.models import *


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_organization = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    round = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    word = models.CharField(max_length=100, default="", blank=True, null=True) 
    create_invoice = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.organization} - ({self.invoice_organization}) ({self.customer})"

    @classmethod
    @transaction.atomic
    def create_invoice(cls, organization, customer, total, date):
        try:
            import inflect
            p = inflect.engine()
            total = float(total)
            sub_total = total  # Assuming sub_total is meant to be the original total
            total_rounded = round(total)
            round_off = total_rounded - sub_total  # Now both are floats, subtraction will work
            words = p.number_to_words(total_rounded)
            
            invoice = cls.objects.create(
                organization=organization,
                customer=customer,
                sub_total=sub_total,
                total=total_rounded,
                round=round_off,
                word=words,
                date=date
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
    payment_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    @transaction.atomic
    def insert_payment_method(cls, invoice, method, payment):
        try:
            payment = float(payment) if payment else 0.0
            cls.objects.create(invoice=invoice, method=method, payment=payment)
        except Exception as e:
            print(f"Error inserting payment: {str(e)}")


class InvoiceProduct(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    registration_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    @transaction.atomic
    def register_invoice_product(cls, organization, invoice, product, rate, quantity, discount, sub_total, gst):
        try:
            discount = int(discount) if discount else 0.0
        except ValueError:
            discount = 0.0

        # Convert 'sub_total' to float, default to 0.0 if empty or invalid
        try:
            quantity = float(quantity) if quantity.strip() else 0.0
        except ValueError:
            quantity = 0.0
        try:
            sub_total = float(sub_total) if sub_total.strip() else 0.0
        except ValueError:
            sub_total = 0.0
        try:
            rate = float(rate) if rate.strip() else 0.0
        except ValueError:
            rate = 0.0
        try:
            gst = float(gst) if gst.strip() else 0.0
        except ValueError:
            gst = 0.0    
        total_before_gst = quantity * rate

        # Apply discount
        gst_rate = total_before_gst * gst/100


        try:
            cls.objects.create(
                organization=organization,
                invoice=invoice,
                product=product,
                gst = gst_rate,
                rate = rate,
                quantity=quantity,
                discount=discount,
                sub_total=sub_total,
            )
        except Exception as e:
            print(f"Error creating Invoice Product: {str(e)}")

    def __str__(self):
        return f"{self.organization} - ({self.invoice}) ({self.product})"
