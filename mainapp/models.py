from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta, date

class categorydb(models.Model):
    Categoryname=models.CharField(max_length=100,blank=True,null=True)
    Description = models.TextField(max_length=100, blank=True, null=True)
    Categoryimage= models.ImageField(upload_to="category", null=True, blank=True)

# Create your models here.
# class productdb(models.Model):
#     Categoryname = models.CharField(max_length=100, null=True, blank=True)
#     Vehiclename = models.CharField(max_length=100, null=True, blank=True)
#     Model = models.IntegerField(null=True, blank=True)
#     Price= models.IntegerField(null=True, blank=True)
#     Specification = models.CharField(max_length=100, null=True, blank=True)
#     Registration = models.CharField(max_length=100, null=True, blank=True)
#     Company = models.CharField(max_length=100, null=True, blank=True)
#     Vehicleimage1 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)
#     Vehicleimage2 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)
#     Vehicleimage3 = models.ImageField(upload_to="vehicle_image", null=True, blank=True)

class subcategorydb(models.Model):
    Categoryname=models.CharField(max_length=100,blank=True,null=True)
    Subcategoryname=models.CharField(max_length=100,blank=True,null=True)
    Description = models.TextField(max_length=100, blank=True, null=True)
class productdb(models.Model):
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
    AdditionalData = models.JSONField(null=True, blank=True)  # Flexible field for category-specific data
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)



    def __str__(self):
        return self.Productname






class ApprovalMode(models.Model):
    auto_approve = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if another instance already exists
        if not self.pk and ApprovalMode.objects.exists():
            raise ValidationError("Only one instance of ApprovalMode is allowed.")
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return "Auto-Approval Enabled" if self.auto_approve else "Auto-Approval Disabled"







class DailyRate(models.Model):
    rate_per_day = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)  # Default 10 rupees/day
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rate: ₹{self.rate_per_day}/day"


class AdPending(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/')
    content = models.ImageField(upload_to='ad_content/',null=True)
    submitted_date = models.DateField(auto_now_add=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class AdApproved(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved_date = models.DateField(auto_now_add=True)
    content = models.ImageField(upload_to='ad_content/',null=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    @property
    def expiry_date(self):
        return self.approved_date + timedelta(days=self.duration)

    def has_expired(self):
        return date.today() > self.expiry_date

    def __str__(self):
        return self.title




# Create your models here.
