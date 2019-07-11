from django.http import JsonResponse


class AuthError:
    class AuthException(Exception):
        def __init__(self, message, errors):
            super(AuthException, self).__init__(message)
            self.errors = errors
            self.message = message

    class ErrorMessage:
        PHONE_NUMBER_NOT_FOUND = 'phone number not found'

    class ErrorCode:
        PHONE_NUMBER_NOT_FOUND = -100


    @classmethod
    def generate_error(cls, message, code):
        return JsonResponse({'error': {'message': message,
                                       'code': code}})