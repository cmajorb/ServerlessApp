# serializers.py
from rest_framework import serializers
from .models import Contract, Tenant, Owner, Property, Payment, Invoice, Deposit, Amendment


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ('id','name','address','phonenumber','email','modified','added')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','name','sitenumber','modified','added')

class ContractSerializer(serializers.ModelSerializer):
    tenant = serializers.CharField(read_only=True,source='tenantid.name')
    owner = serializers.CharField(read_only=True,source='ownerid.name')
    propertyname = serializers.CharField(read_only=True,source='propertyid.name')
    managementfee_p = serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = ('id','active','contractid', 'ownerid','tenantid','tenant','propertyid','propertyname','owner','expdate','increasedate','increasepercentage','baserent','salestax','utilities','managementfee','managementfee_p','modified','added')
    def get_managementfee_p(self,obj):
        return "{:.0%}".format(obj.managementfee)

class TenantSerializer(serializers.ModelSerializer):
    contracts = ContractSerializer(many=True)
    class Meta:
        model = Tenant
        fields = ('id','name','email','contracts','modified','added')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id','invoice','salestax','rent','utilities','modified','added')

class InvoiceSerializer(serializers.ModelSerializer):
    contract = serializers.CharField(read_only=True,source='contractid.contractid')
    payments = PaymentSerializer(many=True)
    rentpaid = serializers.DecimalField(max_digits=10,decimal_places=2)
    utilitiespaid = serializers.DecimalField(max_digits=10,decimal_places=2)
    salestaxpaid = serializers.DecimalField(max_digits=10,decimal_places=2)
    class Meta:
        model = Invoice
        fields = ('id','contractid','rentpaid','salestaxpaid','utilitiespaid','payments','contract','salestaxdue','rentdue','utilitiesdue','date','modified','added')
