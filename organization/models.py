import uuid

from django.db import models, transaction
from django.core.validators import RegexValidator
from credentials.models import Profile


gst_id_validator = RegexValidator(
    regex=r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[A-Z\d]{1}$",
    message="GST ID must be in the format XXAAAAA1111A1Z1",
)


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} {self.name}"


# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True)
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gst_id = models.CharField(
        max_length=15, validators=[gst_id_validator], null=True, blank=True
    )
    address = models.TextField(null=True, blank=True)
    pin_code = models.IntegerField()
    email = models.EmailField(max_length=255)
    contact_number = models.BigIntegerField()
    features = models.ManyToManyField(Role)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @classmethod
    @transaction.atomic
    def create_organization_and_employee(cls, organization_data, user):
        try:
            organization = cls.objects.create(
                name=organization_data["name"],
                email=organization_data["email"],
                gst_id=organization_data["gstin"],
                address=organization_data["address"],
                pin_code=organization_data["pincode"],
                contact_number=organization_data["phone"],
            )

            organization.features.add(Role.objects.get(id=1))
            from hr.models import Employee

            employee = Employee.objects.create(
                profile=user,
                organization=organization,
            )

            employee.roles.add(Role.objects.get(id=1))

            return organization, employee
        except Exception as e:
            print(f"Error creating organization and employee: {str(e)}")
            return None, None
