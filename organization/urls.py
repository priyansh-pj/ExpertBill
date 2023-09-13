from django.urls import path

from .views import *

urlpatterns = [
    path("choice/", organizations, name="organizations"),
    path("apply/", apply_organization, name="organization_apply"),
    path("create/", create_organization, name="organization_create"),
    path(
        "verify/<str:organization_id>", organization_verify, name="organization_verify"
    ),
    path("", organization, name="organization"),
    path("feature/", organization_feature, name="organization_feature"),
]
