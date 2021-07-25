from django.contrib import admin
from .models import Contract, Owner, Tenant, Property

admin.site.register(Contract)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(Property)

# Register your models here.
