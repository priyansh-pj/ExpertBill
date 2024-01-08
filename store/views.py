from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .models import *


@login_required(login_url="login")
def inventory(request):
    if "organization" not in request.session or "role" not in request.session:
        return redirect("organizations")
    organization = request.session["organization"]
    role = request.session["role"]

    data = {
        "title": organization.get("name"),
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "role": ", ".join(role),
        "organization": organization,
        "breadcrumb": [reverse("organization")],
        "products": Product.objects.filter(
            organization=Organization.objects.get(
                org_id=organization.get("organization")
            ), status=True
        ).order_by("name"),
    }
    return render(request, "store/inventory.html", data)


@login_required(login_url="login")
def supplier_details(request):
    if "organization" not in request.session or "role" not in request.session:
        return redirect("organizations")
    organization = request.session["organization"]
    role = request.session["role"]

    data = {
        "title": organization.get("name"),
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "role": ", ".join(role),
        "organization": organization,
        "breadcrumb": [reverse("organization")],
        "suppliers": Supplier.objects.filter(
            organization=Organization.objects.get(
                org_id=organization.get("organization")
            )
        ).order_by("name"),
    }

    return render(request, "store/supplier.html", data)
