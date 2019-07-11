from .db_service_auth import DBServiceAuth
from core.api.rpc.rpc_exception import RPCException


class CheckAuthService:

    def __init__(self, db_service_auth:DBServiceAuth):
        self.db_service_auth = db_service_auth

    def check_auth(self, access_token):
        auth = self.db_service_auth.try_get_auth(access_token=access_token)
        if auth == None or auth.person == None:
            raise RPCException(message='Пользователь не найден!')