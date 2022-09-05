from django.contrib import admin
from django import forms

from .models import Company, User, Office, OfficeHour


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'enabled')
    search_fields = ('name', 'email', 'location')

    def get_queryset(self, request):
        qs = super(OfficeAdmin, self).get_queryset(request)
        try:
            company = request.user.company
            return qs.filter(company=company)
        except:
            return qs

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Office, OfficeAdmin)
admin.site.register(OfficeHour)
