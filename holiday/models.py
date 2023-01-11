from django.db import models
from django.core.exceptions import ValidationError
# from jsonfield import JSONField
from datetime import datetime

# create a model for holiday table with fields id, city_name, data and holidayName
class Holiday(models.Model):

    id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    date = models.DateField()
    holidayName = models.CharField(max_length=50)

# create a class for Admin table with id, admin_name, admin_email and password columns
class Admin(models.Model):

    id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=255)
    admin_email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=50)

# create a class for Cities table with fields id, cityName
class Cities(models.Model):

    id = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=255)
