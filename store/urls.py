from django.urls import path

from .views import *

urlpatterns = [
    path("inventory/", inventory, name="inventory"),
    path("inventory/add", register_product, name="inventory_add"),
    path("inventory/remove", remove_product, name="delete_product"),
    path("product/update/qty", update_qty_product, name="update_qty_product"),
    path("supplier/", supplier_details, name="supplier"),
]
