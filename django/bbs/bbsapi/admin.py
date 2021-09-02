from django.contrib import admin
from .models import Contract, Owner, Tenant, Property, Payment

admin.site.register(Contract)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(Property)
admin.site.register(Payment)

# Register your models here.
