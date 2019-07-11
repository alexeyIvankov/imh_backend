from authorization.api.services.token_service import TokenService
from core.api.rpc.rpc_exception import RPCException
from core.api.rpc.rpc_response_builder import RpcResponseBuilder
from authorization.api.providers.provider_persons import IProviderPersons
from core.api.http.http_exception import HTTPException
from authorization.api.parsers.parser_user_info import ParserUserInfo
from authorization.api.services.db_service_new_person import DBServiceNewPerson
from authorization.api.services.db_service_auth import DBServiceAuth
from datetime import datetime
from core.api.services.service_sms_delivery import ServiceSmsDelivery, ServiceSmsDeliveryException
import random

class AuthController:

    #время ожидания подтверждения номера телефона, в секундах
    TIME_WAIT_VERIFY_PHONE_NUMBER = 120

    def __init__(self,
                 db_service_auth:DBServiceAuth,
                 db_service_new_person:DBServiceNewPerson,
                 token_service: TokenService,
                 sms_delivery_service:ServiceSmsDelivery,
                 provider_person:IProviderPersons):

        self.token_service: TokenService = token_service
        self.provider_person = provider_person
        self.db_service_auth = db_service_auth
        self.db_service_new_person = db_service_new_person
        self.service_sms_delivery = sms_delivery_service

    def send_sms(self, rpc_request):

        # пробуем выдернуть телефон и идентификатор устройства
        try:
            phone = rpc_request.try_get_value_from_params('phone', str)
            country_code = rpc_request.try_get_value_from_params('country_code', str)
            device_id = rpc_request.try_get_value_from_params('deviceId', str)

        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        code = str(random.randint(1000, 9000))

        try:
            self.service_sms_delivery.try_send_sms(phone=phone, sms=code)
        except ServiceSmsDeliveryException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        created_date = datetime.utcnow().timestamp().__round__()
        self.db_service_auth.create_or_update_request_authorization(date_create=str(created_date),code=code, phone=phone, device_id=device_id)

        return RpcResponseBuilder.build_from_success(data={'message':'Проверочный код ' + code + '  успешно отправлен' }).json()


    def authorization(self, rpc_request):

        # пробуем выдернуть телефон и идентификатор устройства
        try:
            phone = rpc_request.try_get_value_from_params('phone', str)
            device_id = rpc_request.try_get_value_from_params('deviceId', str)
            country_code = rpc_request.try_get_value_from_params('country_code', str)
            sms_code = rpc_request.try_get_value_from_params('sms_code', str)
        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        request_authorization = self.db_service_auth.try_get_request_authorization(phone_number=phone)

        if request_authorization == None:
            return RpcResponseBuilder.build_from_error(message='Проверочный код не был отправлен!').json()

        current_date = datetime.utcnow().timestamp().__round__()
        create_date = int(request_authorization.date_create)

        if current_date - create_date > self.TIME_WAIT_VERIFY_PHONE_NUMBER:
            return RpcResponseBuilder.build_from_error(message='Время ожидания истекло! Отправьте код повторно!').json()

        if request_authorization.sms_verification.code != sms_code:
            return RpcResponseBuilder.build_from_error(message='Код не правильный! Попробуйте повторить').json()


        # запрашиваем у стороннего сервиса информацию о пользователе по номеру телефона
        try:
            person_info_json = self.provider_person.get_person_info(phoneNumber=phone, country_code=country_code)
        except HTTPException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        parser = ParserUserInfo(json=person_info_json)

        if parser.is_authorization() == None:
            return RpcResponseBuilder.build_from_error(message='service 1c error!').json()

        if parser.is_authorization() == False:
            if parser.get_organization_comment() != None:
                return RpcResponseBuilder.build_from_error(message=parser.get_organization_comment()).json()
            else:
                return RpcResponseBuilder.build_from_error(message='Пользователь не найден!').json()

        if parser.get_name_person() == None:
            return RpcResponseBuilder.build_from_error(message='service 1c error!').json()

        person = self.db_service_new_person.create_or_update_person(name=parser.get_name_person(), phone_number=phone)

        # organization_name = parser.get_organisation_name()
        # if organization_name != None:
        #     db_service.create_or_update_company(name=organization_name)
        #
        # person_position_title = parser.get_person_position_title()
        # person_position_sub_title = parser.get_person_position_sub_title()
        # person_position_date_receipt = parser.get_person_position_date_receipt()
        #
        # if person_position_title != None and person_position_sub_title != None and person_position_date_receipt != None:
        #     db_service.create_or_update_employee_positions(title=person_position_title, sub_title=person_position_sub_title, date_receipt=person_position_date_receipt)

        access_token = self.token_service.generate_access_token(login=phone, device_id=device_id)
        refresh_token = self.token_service.generate_refresh_token(device_id=device_id)

        person = self.db_service_new_person.create_or_update_auth_tokens(access_token_value=access_token.token,
                                                                        access_token_create_date=access_token.created_date,
                                                                        access_token_expire_date=access_token.expired_date,
                                                                        refresh_token_value=refresh_token.token,
                                                                        refresh_token_create_date=refresh_token.created_date,
                                                                        refresh_token_expire_date=refresh_token.expired_date)

        response = {'account':{'name':person.firstName,
                               'phone':person.phoneNumber,
                               'tokens':{'access': person.tokens.access_token.token,
                                         'refresh':person.tokens.refresh_token.token } }}

        return RpcResponseBuilder.build_from_success(data=response).json()