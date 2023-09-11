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
    # organization = models.ManyToManyField(Organization)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "contact_no"]

    def __str__(self):
        return self.username

    @property
    def status_staff(self):
        return self.is_staff

    # def get_associated_organizations(self):
    #     from organization.models import Organization
    #
    #     return Organization.objects.filter(employees__profile=self)
