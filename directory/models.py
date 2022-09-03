from django.db import models
from django.contrib.gis.db import models


# Company model
class Company(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    commercial_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# User model
class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + ' ' + str(self.last_name)


# Office model
class Office(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    geolocation = models.PointField(srid=4326, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Office hours model
class OfficeHours(models.Model):
    offices = models.ManyToManyField(Office)
    day = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.day


