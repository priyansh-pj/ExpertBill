from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


# Create your views here.
@login_required(login_url="login")
def invoice(request):
    organization = request.session["organization"]
    role = request.session["role"]
    data = {
        "title": organization.get("name"),
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "role": ", ".join(role),
        "organization": organization,
        "breadcrumb": [reverse("organization")],
    }
    return render(request, "bill/invoice/invoice.html", data)
