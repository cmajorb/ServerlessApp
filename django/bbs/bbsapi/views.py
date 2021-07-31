# views.py

from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import ContractSerializer, OwnerSerializer, TenantSerializer, PropertySerializer
from .models import Contract, Owner, Tenant, Property
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.http import HttpResponse
import pandas as pd

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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]
    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        data = pd.read_csv(file_obj)
        print(file_obj)
        file_name = default_storage.save(filename, file_obj)
        # ...
        # do some stuff with uploaded file
        # ...
        return HttpResponse(data['OWNER'][0])

