from persons.models import Person
from authorization.models import Auth
from authorization.models import UserAccessToken
from authorization.models import TokenModel
from social_network.types import *
from django.db import transaction
from django.db import models
from social_network.models import SocialNetworkSite
from company.models import Company
from employee_positions.models import EmployeePositions


class DBServiceNewPerson:

    person:Person = None

    @classmethod
    def try_get_person(self, phone_number: str):
        try:
            person = Person.objects.get(phoneNumber=phone_number)
        except Person.DoesNotExist:
            person = None

        return person

    def create_or_update_person(self, phone_number, name):

        try:
            self.person = Person.objects.get(phoneNumber=phone_number)
        except Person.DoesNotExist:
            self.person = Person.objects.create()

        self.person.phoneNumber = phone_number
        self.person.firstName = name
        self.person.save()

        return self.person

    def create_or_update_auth_tokens(self,
                                     access_token_value:str,
                                     access_token_create_date:str,
                                     access_token_expire_date:str,
                                     refresh_token_value:str,
                                     refresh_token_create_date:str,
                                     refresh_token_expire_date:str):

        access_token_db = UserAccessToken.objects.create()
        access_token_db.token = access_token_value
        access_token_db.createdAt = access_token_create_date
        access_token_db.expiredAt = access_token_expire_date

        refresh_token_db = UserAccessToken.objects.create()
        refresh_token_db.token = refresh_token_value
        refresh_token_db.createdAt = refresh_token_create_date
        refresh_token_db.expiredAt = refresh_token_expire_date

        auth_token_db = Auth.objects.create()
        auth_token_db.access_token = access_token_db
        auth_token_db.refresh_token = refresh_token_db

        access_token_db.save()
        refresh_token_db.save()
        auth_token_db.save()
        self.person.tokens = auth_token_db
        self.person.save()

        return self.person


    def create_or_update_company(self, name):

        try:
            company = Company.objects.get(name=name)
        except Company.DoesNotExist:
            company = Company.objects.create()

        company.name = name
        company.save()
        self.person.company = company
        self.person.save()

        return self.person

    def create_or_update_employee_positions(self, title, sub_title, date_receipt):

        try:
            employee_position = EmployeePositions.objects.get(name=name)
        except EmployeePositions.DoesNotExist:
            employee_position = EmployeePositions.objects.create()

        employee_position.title = title
        employee_position.sub_title = sub_title
        employee_position.date_of_receipt = date_receipt
        employee_position.save()
        self.person.employee_position = employee_position
        self.person.save()

        return self.person

