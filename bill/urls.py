from django.urls import path
from .views import *

urlpatterns = [
    path("invoice/", invoice, name="invoice"),
    path("invoice/list", list_invoice, name="list_invoice"),
]
