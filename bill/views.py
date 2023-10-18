from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse

from store.models import *
from .models import *


# Create your views here.
@login_required(login_url="login")
def invoice(request):
    organization = request.session["organization"]
    role = request.session["role"]
    if request.method == "POST":
        data = invoice_post_data(request.POST)
        print(data)
        register_invoice(data, organization)
        return redirect("invoice")
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
            )
        ).order_by("name"),
    }
    return render(request, "bill/invoice/invoice.html", data)


@login_required(login_url="login")
def list_invoice(request):
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


def register_invoice(data, organization):
    organization = Organization.objects.get(org_id=organization.get("organization"))
    supplier = None
    try:
        supplier = Supplier.objects.get(contact_number=data.get("vendor_phone"))
    except ObjectDoesNotExist:
        supplier = Supplier.register_supplier(
            organization,
            data.get("vendor_name"),
            data.get("vendor_gstin"),
            data.get("vendor_address"),
            data.get("vendor_pincode"),
            data.get("vendor_phone"),
        )

    finally:
        invoice = Invoice.create_invoice(
            organization, supplier, data.get("total"), data.get("invoice_date")
        )

        for payments in data.get("payment"):
            method = payments.get("payment-type")
            payment = payments.get("payment-amt")
            InvoicePayment.insert_payment_method(invoice, method, payment)
        if len(data.get("payment")) == 1 and float(
            data.get("payment")[0].get("payment-amt")
        ) != float(data.get("total")):
            total = float(data.get("total"))
            payment_amt = float(data.get("payment")[0].get("payment-amt"))

            status = total > payment_amt
            method = "Credit" if status else "Advance"
            payment = total - payment_amt if status else payment_amt - total
            InvoicePayment.insert_payment_method(invoice, method, payment)

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
                    items.get("qty"),
                    items.get("rate"),
                    items.get("gst"),
                )
                InvoiceProduct.register_invoice_product(
                    organization,
                    invoice,
                    product,
                    items.get("discount"),
                    items.get("price"),
                )
            else:
                product = Product.objects.get(id=product)
                InvoiceProduct.register_invoice_product(
                    organization,
                    invoice,
                    product,
                    items.get("discount"),
                    items.get("price"),
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


def invoice_post_data(post_data):
    # Initialize the transformed dictionary
    transformed_data = {}

    # Copy simple key-value pairs to the transformed dictionary
    simple_fields = [
        "csrfmiddlewaretoken",
        "vendor_name",
        "vendor_phone",
        "vendor_gstin",
        "vendor_pincode",
        "invoice_date",
        "vendor_city",
        "vendor_state",
        "vendor_address",
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
