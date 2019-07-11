from django.db import models
from company.models import Company
from employee_positions.models import EmployeePositions
from social_network.models import SocialNetwork


class Person(models.Model):
    class Meta:
        verbose_name_plural = 'Все сотрудники'

    tokens = models.OneToOneField(
        'authorization.Auth',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True
    )

    company = models.ForeignKey(
        'company.Company',
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=False
    )

    employee_position = models.ForeignKey(
        'employee_positions.EmployeePositions',
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=False
    )

    social_network = models.ForeignKey(
        'social_network.SocialNetwork',
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=False
    )

    firstName = models.TextField(max_length=100, verbose_name='Имя')
    secondName = models.TextField(max_length=100, verbose_name='Фамилия')
    thirdName = models.TextField(max_length=100, verbose_name='Отчество')
    phoneNumber = models.TextField(max_length=100, verbose_name='Номер телефона')
    address_residence = models.TextField(max_length=300, verbose_name='Адресс', default=None, null=True)

    def __str__(self):
        return self.firstName + ' ' + self.secondName
