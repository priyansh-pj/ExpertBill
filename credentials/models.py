from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_no,
        password=None,
        **extra_fields
    ):
        if not username:
            raise ValueError("The username must be set")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_no=contact_no,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_password(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        user = self.get(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_no,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            username, first_name, last_name, email, contact_no, password, **extra_fields
        )

    def create_staffuser(
        self,
        username,
        first_name,
        last_name,
        email,
        contact_no,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        return self.create_user(
            username, first_name, last_name, email, contact_no, password, **extra_fields
        )


class Profile(AbstractUser):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact_no = models.BigIntegerField()
    password = models.CharField(max_length=255)
    # profile_image = models.ImageField(default='default_user.png', upload_to='/path')
    organization = models.ManyToManyField(to="organization.Organization")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "contact_no"]

    def __str__(self):
        return self.username

    @property
    def status_staff(self):
        return self.is_staff

    def get_associated_organizations(self):
        from organization.models import Organization

        organizations = Organization.objects.filter(
            employees__profile=self, employees__status=True
        ).values("id", "name", "employees__roles__name")

        # Create a dictionary to store the merged results
        org_dict = {}

        for org in organizations:
            org_id = org["id"]

            if org_id in org_dict:
                org_dict[org_id]["roles"].append(org["employees__roles__name"])
            else:
                org_dict[org_id] = {
                    "id": org_id,
                    "name": org["name"],
                    "roles": [org["employees__roles__name"]],
                }

        # Convert the dictionary values back to a list
        merged_organizations = list(org_dict.values())

        return merged_organizations
