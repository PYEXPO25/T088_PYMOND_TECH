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
class seller(models.Model):
    farmername=models.CharField(max_length=20,default="Not Specified")
    farmermobile=models.BigIntegerField(default=0)
    farmerlocation=models.CharField(max_length=20,default="Not")
    cropname=models.CharField(max_length=20)
    quantity=models.IntegerField()
    price=models.IntegerField()
    experience=models.IntegerField()
    def __str__(self):
        return f"{self.cropname} added to sellers"
    
class plantationtips(models.Model):
    cropname=models.CharField(max_length=20)
    choice=models.TextField()
    climate=models.TextField()
    soil=models.TextField()
    seedpreparation=models.TextField()
    plantingprocess=models.TextField()
    fertilizer=models.TextField()
    irrigation=models.TextField()
    weed_and_pest_management=models.TextField()
    harvestingandstorage=models.TextField()
    expectedyield=models.TextField()
    finaltips=models.TextField()
    def __str__(self):
        return f"{self.cropname} added to plantationtips"

class schemes(models.Model):
    schemename=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return f"{self.schemename} added to schemes"

class loan(models.Model):
    reqdocs=models.TextField()
    types=models.TextField()
    benefits=models.TextField()
    how_to_apply=models.TextField()
    def __str__(self):
        return f"Loan added to loan"