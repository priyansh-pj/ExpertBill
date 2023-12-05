from django.urls import path
from .views import *

urlpatterns = [
    path("add_employee/", add_employee, name="add_employee"),
    path("candidate/<int:id>/", candidate, name="candidate"),
    path("remove_candidate/<int:id>/", remove_candidate, name="remove_candidate"),
]
