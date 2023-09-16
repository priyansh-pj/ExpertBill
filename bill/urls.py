from django.urls import path
from .views import *

urlpatterns = [
    path("invoice/", invoice, name="invoice"),
]
