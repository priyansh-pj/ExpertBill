# Generated by Django 4.2.5 on 2023-09-11 20:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("org_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                (
                    "gst_id",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="GST ID must be in the format XXAAAAA1111A1Z1",
                                regex="^\\d{2}[A-Z]{5}\\d{4}[A-Z]{1}[1-9A-Z]{1}Z[A-Z\\d]{1}$",
                            )
                        ],
                    ),
                ),
                ("address", models.TextField(blank=True, null=True)),
                ("pin_code", models.IntegerField()),
                ("email", models.EmailField(max_length=255)),
                ("contact_number", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("features", models.ManyToManyField(to="organization.role")),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("govt_id", models.CharField(blank=True, max_length=25, null=True)),
                ("salary", models.FloatField(blank=True, default=0.0)),
                ("address", models.TextField(blank=True, null=True)),
                ("company_mail", models.EmailField(max_length=255)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="organization.organization",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("roles", models.ManyToManyField(to="organization.role")),
            ],
        ),
        migrations.CreateModel(
            name="AppliedOrganization",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organization.organization",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applicants",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
