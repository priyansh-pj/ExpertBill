from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def organizations(request):
    data = {
        "title": "Organization Choice",
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "organizatons": request.user.get_associated_organizations(),
    }
    print(data)
    return render(request, "organization/choices.html", data)


@login_required(login_url="login")
def apply_organization(request):
    pass


@login_required(login_url="login")
def create_organization(request):
    pass


@login_required(login_url="login")
def organization_verify(request):
    pass


@login_required(login_url="login")
def organization_feature(request):
    pass
