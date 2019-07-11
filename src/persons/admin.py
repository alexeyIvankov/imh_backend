from django.contrib import admin
from .models import Person
from .models import Company


class CompanyMember(admin.ModelAdmin):
    list_display = ['firstName', 'secondName', 'phoneNumber', 'address_residence']
    search_fields = ('firstName', 'secondName', 'phoneNumber', 'address_residence')
    actions = []


admin.site.register(Person, CompanyMember)


