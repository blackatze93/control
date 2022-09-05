import phonenumbers
from django.core.exceptions import ValidationError
from django.db import models
from phonenumbers.phonenumberutil import region_code_for_number
from places.fields import PlacesField
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyCRQFei21_9MtZjEJdx4eHO-6aEkWXkKVk')


# Company model
class Company(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    commercial_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)
    phone = models.CharField(max_length=16)
    location = PlacesField()

    def __str__(self):
        return self.name


# User model
class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=16, help_text='Phone number must be in international format, e.g. +571234567890')
    location = PlacesField()

    def clean(self):
        try:
            phone_country_code = region_code_for_number(phonenumbers.parse(self.phone))
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError({'phone': 'Phone number is not valid'})

        geocode_result = gmaps.reverse_geocode((self.location.latitude, self.location.longitude))
        country_code = ''
        for component in geocode_result[0]['address_components']:
            if 'country' in component['types']:
                country_code = component['short_name']

        if phone_country_code != country_code:
            raise ValidationError({'phone': 'Phone number does not match the country of the location'})


    def __str__(self):
        return str(self.name) + ' ' + str(self.last_name)


# Office model
class Office(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    location = PlacesField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Office hour model
class OfficeHour(models.Model):
    offices = models.ManyToManyField(Office)
    day = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.day


