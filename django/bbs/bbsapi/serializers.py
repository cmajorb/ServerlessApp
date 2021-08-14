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
    tenant = serializers.CharField(read_only=True,source='tenantid.name')
    owner = serializers.CharField(read_only=True,source='ownerid.name')
    propertyname = serializers.CharField(read_only=True,source='propertyid.name')
    managementfee_p = serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = ('id','contractid', 'ownerid','tenantid','tenant','propertyid','propertyname','owner','expdate','increasedate','increasepercentage','baserent','salestax','utilities','managementfee','managementfee_p','modified','added')
    def get_managementfee_p(self,obj):
        return "{:.0%}".format(obj.managementfee)

class TenantSerializer(serializers.ModelSerializer):
    contracts = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tenant
        fields = ('id','name','contracts','modified','added')