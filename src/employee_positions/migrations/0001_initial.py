# Generated by Django 2.1.1 on 2018-12-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePositions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=500, verbose_name='Название должности')),
                ('sub_title', models.TextField(max_length=500, verbose_name='Название отдела')),
                ('date_of_receipt', models.DateField(verbose_name='Дата вступления')),
            ],
            options={
                'verbose_name_plural': 'Все должности',
            },
        ),
    ]
