# serializers.py
from rest_framework import serializers
from .models import Contract, Tenant, Owner, Property




class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ('id','name','address','phonenumber','modified','added')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','name','sitenumber','modified','added')

class ContractSerializer(serializers.ModelSerializer):
    #tenant = TenantSerializer(many=False,read_only=True)
    #tenantname = serializers.SlugRelatedField(many=False, read_only=True,slug_field='tenantname')
    tenant = serializers.CharField(read_only=True,source='tenantid.name')
    owner = serializers.CharField(read_only=True,source='ownerid.name')
    propertyname = serializers.CharField(read_only=True,source='propertyid.name')
    #tenant = serializers.StringRelatedField(many=False)
    class Meta:
        model = Contract
        fields = ('id','contractid', 'ownerid','tenantid','tenant','propertyid','propertyname','owner','expdate','increasedate','increasepercentage','baserent','salestax','utilities','managementfee','modified','added')

class TenantSerializer(serializers.ModelSerializer):
    contracts = serializers.StringRelatedField(many=True)
    #contracts = ContractSerializer(many=True)
    class Meta:
        model = Tenant
        fields = ('id','name','contracts','modified','added')