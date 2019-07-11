from authorization.api.providers.provider_persons import IProviderPersons
from core.api.http.http_exception import HTTPException
from core.api.http.http_code_errors import *
import requests


class ServiceInteracting1C(IProviderPersons):

    HOST_URL = 'http://10.10.47.211/upp_test3_NA/hs/EmployeesData/'

    def get_person_info(self, phoneNumber:str, country_code:str):
        try:
            response = requests.get(url=self.HOST_URL, params={'PhoneNumber':phoneNumber, 'CountryCode':country_code, 'TypeOfService':'GeneralInformation'})
        except:
            raise HTTPException(message='service not available', code=SERVICE_NOT_AVALAIBLE)

        try:
            person_info_json = response.json()
        except:
            raise HTTPException(message='failed parse json', code=FAILED_PARSE_JSON)

        return  person_info_json
