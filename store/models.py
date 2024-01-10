from django.db import models, transaction
from organization.models import Organization
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


gst_id_validator = RegexValidator(
    regex=r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[A-Z\d]{1}$",
    message="GST ID must be in the format XXAAAAA1111A1Z1 (two digits, five letters, four digits, one letter, one digit, one letter, one digit)",
)


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gst_id = models.CharField(
        max_length=15, validators=[gst_id_validator], null=True, blank=True
    )
    address = models.TextField(null=True, blank=True)
    pin_code = models.PositiveIntegerField(
        validators=[MinValueValidator(100000), MaxValueValidator(999999)]
    )
    contact_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.organization}-{self.name}"

    @classmethod
    @transaction.atomic
    def register_supplier(
        cls, organization, name, gst_id, address, pin_code, contact_number
    ):
        try:
            supplier = cls.objects.create(
                organization=organization,
                name=name,
                gst_id=gst_id,
                address=address,
                pin_code=pin_code,
                contact_number=contact_number,
            )
            return supplier
        except Exception as e:
            print(f"Error creating supplier: {str(e)}")

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gst_id = models.CharField(
        max_length=15, validators=[gst_id_validator], null=True, blank=True
    )

    contact_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.organization}-{self.name}"

    @classmethod
    @transaction.atomic
    def register_customer(
        cls, organization, name, gst_id, address, pin_code, contact_number
    ):
        try:
            supplier = cls.objects.create(
                organization=organization,
                name=name,
                gst_id=gst_id,


                contact_number=contact_number,
            )
            return supplier
        except Exception as e:
            print(f"Error creating supplier: {str(e)}")


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=255, default="", blank=True, null=True)
    sku_code = models.CharField(max_length=255, default="", blank=True, null=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    sgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    igst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    gst_included = models.BooleanField(default=False)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    @classmethod
    @transaction.atomic
    def product_register(
        cls,
        organization,
        name,
        barcode,
        description,
        hsn_code,
        sku_code,
        quantity,
        price,
        cgst,

    ):
        try:

            quantity = int(quantity) if quantity else 0
            price = float(price) if price.strip() else 0.0
            cgst = float(cgst) if cgst.strip() else 0.0

            product = cls.objects.create(
                organization=organization,
                name=name,
                barcode=barcode,
                description=description,
                hsn_code=hsn_code,
                sku_code=sku_code,
                quantity=quantity,
                price=price,
                cgst=cgst,
            )
            return product
        except Exception as e:
            print(f"Error creating Product: {str(e)}")

    @classmethod
    @transaction.atomic
    def product_add(
        cls,
        organization,
        name,
        barcode,
        description,
        hsn_code,
        sku_code,
        quantity,
        price,
        cgst,
        sgst,
        igst,
    ):
        try:
            quantity = int(quantity) if quantity.strip() else 0
            price = float(price) if price.strip() else 0.0
            cgst = float(cgst) if cgst.strip() else 0.0
            sgst = float(sgst) if sgst.strip() else 0.0
            igst = float(igst) if igst.strip() else 0.0

            product = cls.objects.create(
                organization=organization,
                name=name,
                barcode=barcode,
                description=description,
                hsn_code=hsn_code,
                sku_code=sku_code,
                quantity=quantity,
                price=price,
                cgst=cgst,
                sgst=sgst,
                igst=igst
            )
            return product
        except Exception as e:
            print(f"Error creating Product: {str(e)}")

    def save(self, *args, **kwargs):
        try:
            if self.quantity < 0:
                self.quantity = 0

            # Ensure cgst, sgst, and igst are converted to float
            self.cgst, self.sgst, self.igst = (
                float(self.cgst) / 100,
                float(self.sgst) / 100,
                float(self.igst) / 100,
            )

            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving Product: {str(e)}")


from bill.models import Invoice


class Expenses(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization} - {self.expense_name} ({self.description})"

    @classmethod
    @transaction.atomic
    def transport_save(cls, name, vehical_number, phone, id, amount, invoice):
        try:
            expense = cls.objects.create(
                type="Transport",
                expense_name=name,
                description=f"Transport Id: {id}, Transport Name: {name}, Transport Phone: {phone}, Vehical Number: {vehical_number}",
                amount=amount,
                invoice=invoice,
            )
            return expense
        except Exception as e:
            print(f"Error creating transport expense: {str(e)}")
