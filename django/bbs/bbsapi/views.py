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
import csv

def get_model_field_names(model, ignore_fields=['content_object']):
    '''
    ::param model is a Django model class
    ::param ignore_fields is a list of field names to ignore by default
    This method gets all model field names (as strings) and returns a list 
    of them ignoring the ones we know don't work (like the 'content_object' field)
    '''
    model_fields = model._meta.get_fields()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names

def get_lookup_fields(model, fields=None):
    '''
    ::param model is a Django model class
    ::param fields is a list of field name strings.
    This method compares the lookups we want vs the lookups
    that are available. It ignores the unavailable fields we passed.
    '''
    model_field_names = get_model_field_names(model)
    if fields is not None:
        '''
        we'll iterate through all the passed field_names
        and verify they are valid by only including the valid ones
        '''
        lookup_fields = []
        for x in fields:
            if "__" in x:
                # the __ is for ForeignKey lookups
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        '''
        No field names were passed, use the default model fields
        '''
        lookup_fields = model_field_names
    return lookup_fields
    
def qs_to_dataset(qs, fields=None):
    '''
    ::param qs is any Django queryset
    ::param fields is a list of field name strings, ignoring non-model field names
    This method is the final step, simply calling the fields we formed on the queryset
    and turning it into a list of dictionaries with key/value pairs.
    '''
    
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))

def convert_to_dataframe(qs, fields=None, index=None):
    '''
    ::param qs is an QuerySet from Django
    ::fields is a list of field names from the Model of the QuerySet
    ::index is the preferred index column we want our dataframe to be set to
    
    Using the methods from above, we can easily build a dataframe
    from this data.
    '''
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df

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

class ReportDownloadView(views.APIView):
    def get(self, request):
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
        )
        qs = Contract.objects.all()
        df = convert_to_dataframe(qs, fields=['id','contractid', 'ownerid','tenantid','tenant','propertyid','propertyname','owner','expdate','increasedate','increasepercentage','baserent','salestax','utilities','managementfee','modified','added'])
        df.to_csv(path_or_buf=response)
        return response