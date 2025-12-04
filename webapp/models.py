from django.db import models
from mainapp.models import productdb
from django.db import models
from django.utils.timezone import now

class pendingdb(models.Model):
    Username=models.CharField(max_length=100, null=True, blank=True)
    Categoryname = models.CharField(max_length=100, null=True, blank=True)
    Subcategoryname = models.CharField(max_length=100, null=True, blank=True)
    Productname = models.CharField(max_length=100, null=True, blank=True)
    Ownername = models.CharField(max_length=100, null=True, blank=True)
    Price = models.IntegerField(null=True, blank=True)
    Mobile = models.IntegerField(null=True, blank=True)
    Location = models.CharField(max_length=100, null=True, blank=True)
    Description = models.CharField(max_length=100, null=True, blank=True)
    Vehicleimage1 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)
    Vehicleimage2 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)
    Vehicleimage3 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)
    AdditionalData = models.JSONField(null=True, blank=True)
class signupdb(models.Model):
    Name = models.CharField(max_length=100, blank=True, null=True)
    Mobile = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    Password = models.CharField(max_length=100, blank=True, null=True)
    Re_password = models.CharField(max_length=100, blank=True, null=True)
class myitemdb(models.Model):
    Username = models.CharField(max_length=100, blank=True, null=True)
    Productname = models.CharField(max_length=100, blank=True, null=True)
    created_at =models.CharField(max_length=100, blank=True, null=True)

class cartdb(models.Model):
    Username = models.CharField(max_length=100, blank=True, null=True)
    Productname = models.CharField(max_length=100, blank=True, null=True)
    Price = models.IntegerField(blank=True, null=True)
    productdb_id= models.IntegerField(blank=True, null=True)

class contactdb(models.Model):
    Name= models.CharField(max_length=100,blank=True,null=True)
    Mobile = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    Message = models.CharField(max_length=100, blank=True, null=True)








class Message(models.Model):
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)  # Store receiver's username or ID
    product = models.ForeignKey('mainapp.productdb', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.timestamp}"







