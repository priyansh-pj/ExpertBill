from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import *


# Create your views here.
@login_required(login_url="login")
def add_employee(request):
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
        "candidates": AppliedOrganization.objects.filter(
            organization=Organization.objects.get(
                org_id=organization.get("organization")
            )
        ).order_by("time"),
    }
    return render(request, "hr/add_employee.html", data)


@login_required(login_url="login")
def candidate(request, id):
    if "organization" not in request.session or "role" not in request.session:
        return redirect("organizations")

    organization = request.session["organization"]
    role = request.session["role"]
    if request.method == "POST":
        application = get_object_or_404(
            AppliedOrganization, id=request.POST.get("application_id")
        )
        employee = Employee(
            profile=application.profile,
            organization=application.organization,
            salary=request.POST.get("salary"),
        )
        employee.save()
        application.delete()
        return redirect("add_employee")
    data = {
        "title": organization.get("name"),
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "role": ", ".join(role),
        "organization": organization,
        "breadcrumb": [reverse("organization"), reverse("add_employee")],
        "candidate": get_object_or_404(AppliedOrganization, id=id),
        "roles": Role.objects.exclude(id=1),
    }
    return render(request, "hr/manage_candidate.html", data)


def remove_candidate(request, id):
    if "organization" not in request.session or "role" not in request.session:
        return redirect("organizations")
    applied_organization = get_object_or_404(AppliedOrganization, id=id)
    applied_organization.delete()
    return redirect("add_employee")
