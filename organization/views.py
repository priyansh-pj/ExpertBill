from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *


# Create your views here.
@login_required(login_url="login")
def organizations(request):
    request.session.pop("organization", None)
    request.session.pop("role", None)
    data = {
        "title": "Organization Choice",
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "organizations": request.user.get_associated_organizations(),
    }
    print(data)
    return render(request, "organization/choices.html", data)


@login_required(login_url="login")
def apply_organization(request):
    data = {
        "title": "Organization Apply",
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "breadcrumb": [reverse("organizations")],
    }
    if request.method == "POST":
        organization_id = request.POST.get("id")
        org = AppliedOrganization.apply(request.user, organization_id)
        return redirect("organizations")

    return render(request, "organization/apply.html", data)


@login_required(login_url="login")
def create_organization(request):
    data = {
        "title": "Organization Create",
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "breadcrumb": [reverse("organizations")],
    }
    if request.method == "POST":
        organization = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "gstin": request.POST.get("gstin"),
            "phone": request.POST.get("phone"),
            "city": request.POST.get("city"),
            "state": request.POST.get("state"),
            "pincode": request.POST.get("pincode"),
            "address": request.POST.get("address"),
        }
        Organization.create(organization, request.user)
        print(organization)
        return redirect("organization_create")
    return render(request, "organization/create.html", data)


@login_required(login_url="login")
def organization_feature(request):
    pass


@login_required(login_url="login")
def organization_verify(request, organization_id):
    organization = Organization.objects.get(id=organization_id)
    role = Employee.validate_organization(request.user, organization)
    print(role)
    if not role:
        return redirect("organizations")

    request.session["organization"] = organization
    request.session["role"] = role
    return redirect("organizations")
