from django.db import models
# Create your models here.

class Users(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Profile_Picture = models.ImageField()
    Username = models.CharField(max_length=200)
    Email_id = models.EmailField()
    Password = models.CharField(max_length=1000)
    Role = models.CharField(max_length=100, null=True)

class Address(models.Model):
    Username = models.ForeignKey(Users, on_delete=models.CASCADE)
    Line = models.CharField(max_length=1000)
    city = models.CharField(max_length= 1000)
    state = models.CharField(max_length=1000)
    pincode = models.IntegerField(max_length=100)