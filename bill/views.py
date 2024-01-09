from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from store.models import *
from .models import *


# Create your views here.
@login_required(login_url="login")
def invoice(request):
    if "organization" not in request.session or "role" not in request.session:
        return redirect("organizations")
    organization = request.session["organization"]
    role = request.session["role"]
    if request.method == "POST":
        data = invoice_post_data(request.POST)
        print(data)
        invoice = register_invoice(data, organization)
        return redirect("invoice_print", invoice)
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
            ), status= True
        ).order_by("name"),
    }

    return render(request, "bill/invoice/invoice.html", data)


def invoice_print(request, id):

    organization = Organization.objects.get(org_id=request.session["organization"].get("organization"))
    invoice = Invoice.objects.get(id=id, organization=organization)
    invoiceProducts = InvoiceProduct.objects.filter(invoice= invoice, organization= organization)
    data = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "organization": organization,
        "invoice": invoice,
        "products" : invoiceProducts,
    }
    return render(request, "bill/invoice/print.html", data)



@login_required(login_url="login")
def list_invoice(request):
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
        "invoices": Invoice.objects.filter(
            organization=Organization.objects.get(
                org_id=organization.get("organization")
            )
        ).order_by("invoice_organization"),
    }
    return render(request, "bill/invoice/list.html", data)


@csrf_exempt
def customer_details(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        contact = request_data.get("contact")
        customer_details = Customer.objects.values('name', 'gst_id', 'address', 'pin_code', 'contact_number').filter(contact_number=contact).first()

        if customer_details:
            # Customer details found, return a JSON response
            data = {
                'name': customer_details['name'],
                'gst_id': customer_details['gst_id'],
                'address': customer_details['address'],
                'pin_code': customer_details['pin_code'],
                'contact_number': customer_details['contact_number']
            }
            return JsonResponse(data, status=200)
        else:
            # Customer details not found, return a JSON response
            data = {
                'message': 'Customer not found'
            }
            return JsonResponse(data, status=404)
    else:
        data = {
            'message': 'Only POST Method'
        }
        return JsonResponse(data, status=405)

@csrf_exempt
def product_details(request):
    if request.method == "POST":
        try:

            request_data = json.loads(request.body)
            
        except json.JSONDecodeError:
            data = {
                'message': 'Invalid JSON data'
            }
            return JsonResponse(data, status=400)

        organization_id = request_data.get("organization")

        try:
            organization = Organization.objects.get(org_id=organization_id)
        except Organization.DoesNotExist:

            data = {
                'message': 'Invalid Organization'
            }
            return JsonResponse(data, status=400)

        product_id = request_data.get("product_id")
        barcode = request_data.get("barcode")

        if product_id:
            field_name = "id"
            value = product_id
        elif barcode:
            field_name = "barcode"
            value = barcode
        else:
            data = {
                'message': 'Invalid Request'
            }


            return JsonResponse(data, status=400)

        product = Product.objects.filter(organization=organization, **{field_name: value}).values().first()


        if product:
            data = product
            return JsonResponse(data, status=200)
        else:
            data = {
                'message': 'Product not found'
            }
            return JsonResponse(data, status=404)
    else:
        data = {
            'message': 'Only POST Method'
        }
        return JsonResponse(data, status=405)


# Helper Functions
@transaction.atomic
def register_invoice(data, organization):
    organization = Organization.objects.get(org_id=organization.get("organization"))
    customer = None
    try:
        customer = Customer.objects.get(contact_number=data.get("customer_phone"))
    except ObjectDoesNotExist:
        customer = Customer.register_customer(
            organization,
            data.get("customer_name"),
            data.get("customer_gstin"),
            data.get("customer_address"),
            data.get("customer_pincode"),
            data.get("customer_phone"),
        )

    finally:
        invoice = Invoice.create_invoice(
            organization, customer, data.get("total"), data.get("invoice_date")
        )

        for payments in data.get("payment"):
            method = payments.get("payment-type")
            payment = payments.get("payment-amt")
            InvoicePayment.insert_payment_method(invoice, method, payment)
        if len(data.get("payment")) == 1 and float(data.get("payment")[0].get("payment-amt")) != float(data.get("total")):
            total = float(data.get("total"))
            payment_amt = float(data.get("payment")[0].get("payment-amt"))

            status = total > payment_amt
            method = "Credit" if status else "Advance"
            payment = total - payment_amt if status else payment_amt - total
            InvoicePayment.insert_payment_method(invoice, method, payment)
        

        # Issue 
        for items in data.get("invoice_items"):
            product = items.get("product", False)
            if not product:
                product = Product.product_register(
                    organization,
                    items.get("name"),
                    items.get("barcode"),
                    items.get("description"),
                    items.get("hsn"),
                    items.get("sku"),
                    0,
                    items.get("rate"),
                    items.get("gst"),
                )
                product.status = False
                product.save()
                InvoiceProduct.register_invoice_product(
                    organization,
                    invoice,
                    product,
                    items.get("rate") or 0 ,
                    items.get("qty") or 0 ,
                    items.get("discount") or 0,
                    items.get("price") or 0,
                    items.get("gst") or 0,
                )
            else:
                product = Product.objects.get(id=product)
                product.quantity -= int(items.get("qty")) or 0
                product.save()
                InvoiceProduct.register_invoice_product(
                    organization,
                    invoice,
                    product,
                    items.get("rate") or 0 ,
                    items.get("qty") or 0 ,
                    items.get("discount") or 0,
                    items.get("price") or 0,
                    items.get("gst") or 0,
                )
                

        if data.get("transport_status") == "on":
            transport = data.get("transport")
            Expenses.transport_save(
                name=transport.get("transporter_name"),
                vehical_number=transport.get("transporter_vehicle"),
                phone=transport.get("transporter_phone"),
                id=transport.get("transporter_id"),
                    amount=transport.get("transport_amt"),
                    invoice=invoice,
            )
    return invoice.id


def invoice_post_data(post_data):
    # Initialize the transformed dictionary
    transformed_data = {}

    # Copy simple key-value pairs to the transformed dictionary
    simple_fields = [
        "csrfmiddlewaretoken",
        "customer_name",
        "customer_phone",
        "customer_gstin",
        "customer_pincode",
        "invoice_date",
        "customer_city",
        "customer_state",
        "customer_address",
        "total",
        "partial-payment",
        "transport_status",
    ]

    for field in simple_fields:
        transformed_data[field] = post_data.get(field, "")

    if transformed_data.get("transport_status", ""):
        transformed_data["transport"] = {
            "transporter_name": post_data.get("transporter_name", ""),
            "transporter_phone": post_data.get("transporter_phone", ""),
            "transporter_vehicle": post_data.get("transporter_vehicle", ""),
            "transporter_id": post_data.get("transporter_id", ""),
            "transport_amt": post_data.get("transport_amt", ""),
        }
    # Process invoice_items and payment arrays
    invoice_items = []
    payment = []

    # Iterate over the POST data to find keys related to invoice_items and payment
    for key, value in post_data.items():
        if key.startswith("invoice_items["):
            index = key.split("[")[1].split("]")[0]  # Extract the index from the key
            field_name = key.split("[")[2].split("]")[
                0
            ]  # Extract the field name from the key

            # Ensure the index is valid
            try:
                index = int(index)
            except ValueError:
                continue

            # Create a new item dictionary if it doesn't exist yet
            if len(invoice_items) <= index:
                invoice_items.append({})

            # Assign the value to the appropriate field within the item dictionary
            invoice_items[index][field_name] = value

        elif key.startswith("payment["):
            index = key.split("[")[1].split("]")[0]
            field_name = key.split("[")[2].split("]")[0]

            try:
                index = int(index)
            except ValueError:
                continue

            if len(payment) <= index:
                payment.append({})
            payment[index][field_name] = value

    transformed_data["invoice_items"] = invoice_items
    transformed_data["payment"] = payment

    return transformed_data


