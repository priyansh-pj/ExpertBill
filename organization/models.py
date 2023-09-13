import uuid

from django.db import models, transaction
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
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
    def create(cls, organization, user):
        organization = cls.objects.create(
            name=organization["name"],
            email=organization["email"],
            gst_id=organization["gstin"],
            address=organization["address"],
            pin_code=organization["pincode"],
            contact_number=organization["phone"],
        )
        organization.features.add(Role.objects.get(id=1))

        employee = Employee.objects.create(
            profile=user,
            organization=organization,
        )

        employee.roles.add(Role.objects.get(id=1))


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="employees"
    )
    govt_id = models.CharField(max_length=25, null=True, blank=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="employees"
    )
    roles = models.ManyToManyField(Role)
    salary = models.FloatField(default=0.00, blank=True)
    address = models.TextField(null=True, blank=True)
    company_mail = models.EmailField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Employee: {self.profile.username} ({self.organization.name})"

    @classmethod
    def validate_organization(cls, user, organization):
        try:
            employee = Employee.objects.get(profile=user, organization=organization)
            roles = [role.get("name") for role in employee.roles.values("name").all()]
            return roles
        except Employee.DoesNotExist:
            return None


class AppliedOrganization(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="applicants"
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization} - {self.profile}"

    @classmethod
    @transaction.atomic
    def apply(cls, user, organization):
        organization = Organization.objects.get(org_id=organization)
        return cls.objects.create(profile=user, organization=organization)
