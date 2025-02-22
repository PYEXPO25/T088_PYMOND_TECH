from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"

class Croplist(models.Model):
    cropname=models.CharField(max_length=50)
    farmername=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Added Crop {self.cropname} to {self.farmername}"
    
class disease(models.Model):
    cropname=models.CharField(max_length=50)
    diseasename=models.CharField(max_length=50)
    diseasetype=models.CharField(max_length=20)
    image1=models.ImageField(default='default.png')
    image2=models.ImageField(default='default.png',blank=True)
    symptoms=models.TextField()
    preventivemeasures=models.TextField()
    causedby=models.TextField()
    stage=models.CharField(max_length=50)
    def __str__(self):
        return f"Disease {self.diseasename} added to {self.cropname}"
class location(models.Model):
    Location=models.CharField(max_length=50)
    phonenumber=models.BigIntegerField(null=True)
    farmername=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f"Location {self.Location}"
class fertilizerss(models.Model):
    cropname=models.CharField(max_length=20)
    fertilizer=models.TextField()
    howtouse=models.TextField()
    def __str__(self):
        return f"Fertilize added to {self.cropname}"
class sellers(models.Model):
    cropname=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    experience=models.IntegerField()
    def __str__(self):
        return f"{self.cropname} added to sellers"
class merchant(models.Model):
    username=models.CharField(max_length=20)
    password=models.TextField()
    email=models.EmailField()
    contact=models.BigIntegerField()
    location=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.username} added to merchant"
    