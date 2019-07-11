from django.db import models

class EmployeePositions(models.Model):
    class Meta:
        verbose_name_plural = 'Все должности'

    title = models.TextField(max_length=500, verbose_name='Название должности')
    sub_title = models.TextField(max_length=500, verbose_name='Название отдела')
    date_of_receipt = models.DateField(verbose_name='Дата вступления')

    def __str__(self):
        return self.title


# Create your models here.
