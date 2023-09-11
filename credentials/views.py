from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as Login, logout as Logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def login(request):
    if request.user.is_authenticated:
        return redirect("organizations")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            Login(request, user)
            return redirect("organizations")
        else:
            messages.warning(request, "Invalid credentials")

        return redirect("login")

    return render(request, "authentication/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("organizations")

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        contact_number = request.POST.get("phone")
        password = request.POST.get("password")
        try:
            profile = Profile.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact_no=contact_number,
                password=password,
            )
            Login(request, profile)

            return redirect("organizations")
        except Exception as e:
            messages.warning(request, f"Unable to create account {e}")

        return redirect("register")

    return render(request, "authentication/register.html")


@login_required(login_url="login")
def logout(request):
    Logout(request)
    return redirect("login")
