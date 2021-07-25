# views.py

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ContractSerializer, OwnerSerializer, TenantSerializer, PropertySerializer
from .models import Contract, Owner, Tenant, Property

# Create your views here.

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('id')
    serializer_class = ContractSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by('id')
    serializer_class = OwnerSerializer

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all().order_by('id')
    serializer_class = TenantSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('id')
    serializer_class = PropertySerializer