from django.db import models


class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Все компании'

    name = models.TextField(max_length=100, verbose_name='Название')
    address_location = models.TextField(max_length=300, verbose_name='Адресс')


    def __str__(self):
        return self.name
