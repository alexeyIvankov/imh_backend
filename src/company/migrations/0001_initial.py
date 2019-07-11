# Generated by Django 2.1.1 on 2018-12-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100, verbose_name='Название')),
                ('address_location', models.TextField(max_length=300, verbose_name='Адресс')),
            ],
            options={
                'verbose_name_plural': 'Все компании',
            },
        ),
    ]
