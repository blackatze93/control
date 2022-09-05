from pprint import pprint

from django.contrib import admin
import phonenumbers
import googlemaps
from datetime import datetime
from phonenumbers.phonenumberutil import region_code_for_number
from .models import Company, User, Office, OfficeHour

gmaps = googlemaps.Client(key='AIzaSyCRQFei21_9MtZjEJdx4eHO-6aEkWXkKVk')


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'enabled')
    search_fields = ('name', 'email', 'location')

    def get_queryset(self, request):
        qs = super(OfficeAdmin, self).get_queryset(request)
        print(request.user)
        phone_country_code = region_code_for_number(phonenumbers.parse('+571234561234'))

        location = User.objects.get(pk=1).location

        geocode_result = gmaps.reverse_geocode((location.latitude, location.longitude))
        country_code = ''
        for component in geocode_result[0]['address_components']:
            if 'country' in component['types']:
                country_code = component['short_name']

        print(phone_country_code)
        print(country_code)
        if phone_country_code != country_code:
            print('no es igual')
        else:
            print('es igual')

        return qs.filter(company=1)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'phone', 'company', 'location')
    search_fields = ('name', 'last_name', 'email', 'phone', 'company', 'location')



admin.site.register(Company)
admin.site.register(User, UserAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(OfficeHour)
