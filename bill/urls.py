from django.urls import path
from .views import *

urlpatterns = [
    path("invoice/", invoice, name="invoice"),
    path("invoice/list", list_invoice, name="list_invoice"),
    path("invoice/print/<str:id>", invoice_print, name="invoice_print"),
    path("fetch_customer", customer_details, name="fetch_customer" ),
    path("fetch_product", product_details, name="fetch_product" )
]
