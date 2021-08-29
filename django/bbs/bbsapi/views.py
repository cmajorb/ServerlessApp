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
from django_pandas.io import read_frame
from datetime import datetime
from dateutil.relativedelta import relativedelta

def generate_report(startdate,enddate):
    qs = Contract.objects.all()
    df = read_frame(qs)

    currentdate = startdate

    #df = pd.read_csv('report-12.csv')
    df = df.dropna(subset=['increasedate', 'increasepercentage'])
    df['increasedate'] = pd.to_datetime(df['increasedate'])
    df['adj'] = 13 - df['increasedate'].dt.month

    while currentdate <= enddate:
        df['current'] = currentdate
        df['adjusted'] = df.apply(lambda x: x['current'] + pd.DateOffset(months = x['adj']), axis=1)
        col = str(currentdate.month) + "/" + str(currentdate.year)
        #mask = df['increasedate'].dt.month == month
        #df.loc[mask, 'baserent'] = df['baserent'] * ((1 + df['increasepercentage']) ** ((year - df['increasedate'].dt.year)+1))
        rent = df['baserent'] * ((1 + df['increasepercentage']) ** ((df['adjusted'].dt.year - df['increasedate'].dt.year)))
        management_fee = df['managementfee'] * rent        
        df[col + ' rent'] = rent
        df[col + ' management fee'] = management_fee
        df[col + ' total'] = rent + management_fee + df['salestax'] + df['utilities']   
        currentdate = currentdate + relativedelta(months=+1)

    #df.filter(regex='rent')

    df = df.drop(columns=['adj', 'current','adjusted','id'])
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
        
        startdate = datetime(year=2021, month=1, day=1)
        enddate = datetime(year=2021, month=12, day=1)
        df = generate_report(startdate,enddate)
        

        df.to_csv(path_or_buf=response)
        return response