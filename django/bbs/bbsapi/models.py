# models.py
from django.db import models

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60,blank=True)
    phonenumber = models.CharField(max_length=60,blank=True)
    email = models.CharField(max_length=60,blank=True)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=60,blank=True)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    sitenumber = models.CharField(max_length=60)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

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

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    contractid = models.ForeignKey(Contract,on_delete=models.CASCADE)
    salestax = models.DecimalField(max_digits=10,decimal_places=2)
    rent = models.DecimalField(max_digits=10,decimal_places=2)
    utilities = models.DecimalField(max_digits=10,decimal_places=2)
    paymentdate= models.DateField(null=True)
    modified = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.contractid) + '(' + str(self.id) + ')'