from django.db import models
from accounts.models import User

# Create your models here.

class Locate(models.Model):
    location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.DecimalField()

    def __str__(self):
        return f"{self.location} - {self.destination}"