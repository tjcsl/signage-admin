from django.db import models

# Create your models here.

class Sign(models.Model):
    name = models.CharField(max_length = 80)
    hostname = models.CharField(max_length = 80)
    landscape = models.BooleanField(default = True)
