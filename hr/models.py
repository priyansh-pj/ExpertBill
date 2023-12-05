from django.db import models, transaction
from credentials.models import Profile
from organization.models import Organization, Role


# Create your models here.
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
    company_mail = models.EmailField(max_length=255, null=True, blank=True)
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
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization} - {self.profile}"

    @classmethod
    @transaction.atomic
    def apply(cls, user, organization):
        organization = Organization.objects.get(org_id=organization)
        return cls.objects.create(profile=user, organization=organization)
