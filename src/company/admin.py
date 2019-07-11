from django.contrib import admin
from .models import Company

class CompanyInfo(admin.ModelAdmin):
    list_display = ['name', 'address_location']
    search_fields = ('name', 'address_location')
    actions = []

admin.site.register(Company, CompanyInfo)
