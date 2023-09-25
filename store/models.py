from django.db import models, transaction
from organization.models import Organization
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


gst_id_validator = RegexValidator(
    regex=r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[A-Z\d]{1}$",
    message="GST ID must be in the format XXAAAAA1111A1Z1",
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
    contact_number = models.BigIntegerField(
        validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)],
        unique=True,
    )
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


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    hsn_code = models.CharField(max_length=255, default="", blank=True, null=True)
    sku_code = models.CharField(max_length=255, default="", blank=True, null=True)
    quantity = models.IntegerField(default=0)

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
            product = cls.objects.create(
                organization=organization,
                name=name,
                barcode=barcode,
                description=description,
                hsn_code=hsn_code,
                sku_code=sku_code,
                quantity=int(quantity) if quantity.isdigit() else 0,
                price=float(price) if price.replace(".", "").isdigit() else 0.0,
                cgst=int(cgst) if cgst.isdigit() else 0,
            )
            return product
        except Exception as e:
            print(f"Error creating Product: {str(e)}")

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            self.quantity = 0
        self.cgst, self.sgst, self.igst = (
            self.cgst / 100,
            self.sgst / 100,
            self.igst / 100,
        )
        super().save(*args, **kwargs)
