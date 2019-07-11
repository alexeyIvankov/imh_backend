import os
import django
from django import db
from django.contrib.auth.management.commands.createsuperuser import get_user_model

NAME_SUPER_USER = 'admin'
EMAIL_SUPER_USER = 'admin'
PASSWORD_SUPER_USER = 'admin'


def initial_environ():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'imh_corp_server.settings'

def setup_django():
    django.setup()

def create_superuser_if_need():
    if get_user_model().objects.filter(username='admin'):
        print('Super user already exists. SKIPPING...')
    else:
        print('Creating super user...')
        get_user_model()._default_manager.db_manager().create_superuser(username=NAME_SUPER_USER, email=EMAIL_SUPER_USER,
                                                                        password=PASSWORD_SUPER_USER)
        print('Super user created...')


initial_environ()
setup_django()
create_superuser_if_need()

