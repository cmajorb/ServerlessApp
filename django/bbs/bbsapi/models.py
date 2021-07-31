# models.py
from django.db import models

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60,blank=True)
    phonenumber = models.CharField(max_length=60,blank=True)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + '(' + str(self.id) + ')'

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + '(' + str(self.id) + ')'

class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    sitenumber = models.CharField(max_length=60)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name + '(' + str(self.id) + ')'

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    contractid = models.CharField(max_length=60)
    tenantid = models.ForeignKey(Tenant,related_name='contracts',on_delete=models.CASCADE)
    propertyid = models.ForeignKey(Property,on_delete=models.CASCADE)
    ownerid = models.ForeignKey(Owner,on_delete=models.CASCADE)
    expdate = models.DateField(null=True)
    increasedate= models.DateField(null=True)
    increasepercentage = models.DecimalField(max_digits=5,decimal_places=2)
    salestax = models.DecimalField(max_digits=10,decimal_places=2)
    baserent = models.DecimalField(max_digits=10,decimal_places=2)
    utilities = models.DecimalField(max_digits=10,decimal_places=2)
    managementfee= models.DecimalField(max_digits=10,decimal_places=2)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.contractid