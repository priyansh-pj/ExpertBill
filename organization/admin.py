from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Organization)
admin.site.register(AppliedOrganization)
admin.site.register(Role)
admin.site.register(Employee)
