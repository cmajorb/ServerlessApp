from django.contrib import admin
from .models import Contract, Owner, Tenant, Property, Payment, Invoice

admin.site.register(Contract)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(Property)
admin.site.register(Payment)
admin.site.register(Invoice)

# Register your models here.
