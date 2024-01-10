from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

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
def register_product(request):
    print("url triggers")
    if request.method == "POST":
        print(request.POST)
        gst_included = True if request.POST.get('gst_included') == "no" else False 
        organization = Organization.objects.get(org_id=request.session["organization"].get("organization"))
        Product.product_add(organization, request.POST.get('name'), request.POST.get('barcode'),request.POST.get('description'), request.POST.get('hsn_code'), request.POST.get('sku_code'), request.POST.get('quantity'), request.POST.get('price'), request.POST.get('cgst'), request.POST.get('sgst'), request.POST.get('igst'), gst_included)
    return redirect('inventory')

@csrf_exempt
def remove_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        product = request_data.get("id")
        organization = Organization.objects.get(org_id=request.session["organization"].get("organization"))

        products = Product.objects.get(id=product, organization= organization)

        if products:
            products.status=False
            products.save()
            data = {
                'message': 'Success'
            }
            return JsonResponse(data, status=200)
        else:
            # Customer details not found, return a JSON response
            data = {
                'message': 'Product not found'
            }
            return JsonResponse(data, status=300)
    else:
        data = {
            'message': 'Only POST Method'
        }
        return JsonResponse(data, status=405)
    
@csrf_exempt
def update_qty_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        product = request_data.get("id")
        qty = request_data.get("qty")
        organization = Organization.objects.get(org_id=request.session["organization"].get("organization"))

        products = Product.objects.get(id=product, organization= organization)

        if products:
            products.quantity = int(qty)
            print(qty)

            print(products.quantity)
            products.save()
            data = {
                'message': 'Success'
            }
            return JsonResponse(data, status=200)
        else:
            # Customer details not found, return a JSON response
            data = {
                'message': 'Product not found'
            }
            return JsonResponse(data, status=300)
    else:
        data = {
            'message': 'Only POST Method'
        }
        return JsonResponse(data, status=405)


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
