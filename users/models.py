from django.db import models

from django.contrib.auth.models import User
from django.db.models.base import Model


class Adress(models.Model):
    
    receiver=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
   
    postal_code=models.CharField(max_length=8)
    city=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    contact=models.IntegerField()
    nif=models.IntegerField(blank=True, null=True)

class Profile(models.Model):
    user=models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    
    adress=models.OneToOneField(Adress,related_name="adress", on_delete=models.CASCADE,null=True, blank=True)
    adress_billing=models.OneToOneField(Adress,related_name="adress_billing", on_delete=models.CASCADE,null=True, blank=True)

