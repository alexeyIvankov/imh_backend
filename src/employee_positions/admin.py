from django.contrib import admin
from .models import EmployeePositions


class EmployeePositionsInfo(admin.ModelAdmin):
    list_display = ['title', 'date_of_receipt']
    search_fields = ('title', 'date_of_receipt')
    actions = []

admin.site.register(EmployeePositions, EmployeePositionsInfo)

# Register your models here.
