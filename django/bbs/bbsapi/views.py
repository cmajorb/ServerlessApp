# views.py

from django.shortcuts import render
from rest_framework import viewsets, views
from .serializers import ContractSerializer, OwnerSerializer, TenantSerializer, PropertySerializer, PaymentSerializer
from .models import Contract, Owner, Tenant, Property, Payment
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.http import HttpResponse
import pandas as pd
import csv
from django_pandas.io import read_frame
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

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
        df['monthdays'] = calendar.monthrange(currentdate.year,currentdate.month)[1]
        col = str(currentdate.month) + "/" + str(currentdate.year)
        #mask = df['increasedate'].dt.month == month
        #df.loc[mask, 'baserent'] = df['baserent'] * ((1 + df['increasepercentage']) ** ((year - df['increasedate'].dt.year)+1))
        df['newrent'] = df['baserent'] * ((1 + df['increasepercentage']) ** ((df['adjusted'].dt.year - df['increasedate'].dt.year)))
        df.loc[df['increasedate'].dt.month == currentdate.month,'newrent'] = ((df['baserent'] * (df['increasedate'].dt.day - 1) * (((1 + df['increasepercentage']) ** ((df['adjusted'].dt.year - df['increasedate'].dt.year - 1))) - ((1 + df['increasepercentage']) ** ((df['adjusted'].dt.year - df['increasedate'].dt.year)))) ) / df['monthdays'] ) + df['baserent'] * ((1 + df['increasepercentage']) ** ((df['adjusted'].dt.year - df['increasedate'].dt.year)))
        management_fee = df['managementfee'] * df['newrent']        
        df[col + ' rent'] = df['newrent']
        df[col + ' management fee'] = management_fee
        df[col + ' total'] = df['newrent'] + management_fee + df['salestax'] + df['utilities']   
        currentdate = currentdate + relativedelta(months=+1)

        #df.filter(regex='rent')

    df = df.drop(columns=['adj', 'current','adjusted','id','newrent','monthdays'])
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

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer

class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]
    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        payments = pd.read_csv(file_obj)
        qs = Contract.objects.all()
        df = read_frame(qs)
        payments = payments.merge(df, on='contractid', how='inner')

        for payment in payments.itertuples():
            payment = Payment.objects.create(contractid=Contract.objects.get(id=int(payment.id)),salestax=payment.salestax1,rent=payment.rent1,utilities=payment.utilities1,paymentdate=payment.paymentdate)
        #file_name = default_storage.save(filename, file_obj)
 
        return HttpResponse("It worked!")

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