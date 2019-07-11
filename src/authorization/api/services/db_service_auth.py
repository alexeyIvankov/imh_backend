from authorization.models import RequestAuthorization, SmsVerification, Auth, UserAccessToken


class DBServiceAuth:

    def create_or_update_request_authorization(self,
                                     date_create,
                                     code,
                                     phone,
                                     device_id):
        try:
            request_authorization = RequestAuthorization.objects.get(phone=phone)
        except RequestAuthorization.DoesNotExist:
            request_authorization = RequestAuthorization.objects.create()

        request_authorization.date_create = date_create
        request_authorization.phone = phone

        request_authorization.sms_verification = SmsVerification.objects.create()
        request_authorization.sms_verification.date_send = date_create
        request_authorization.sms_verification.device_id = device_id
        request_authorization.sms_verification.phone = phone
        request_authorization.sms_verification.code = code

        request_authorization.sms_verification.save()
        request_authorization.save()

    def try_get_request_authorization(self, phone_number: str):

        try:
            request_authorization = RequestAuthorization.objects.get(phone=phone_number)
        except RequestAuthorization.DoesNotExist:
            request_authorization = None

        return request_authorization

    def try_get_auth(self, access_token):
        try:
            user_access = UserAccessToken.objects.get(token=access_token)
            auth = user_access.access_token
        except UserAccessToken.DoesNotExist:
            auth = None

        return auth

