from .rpc_keys import RpcKeys
from .rpc_exception import RPCException
from .rpc_code_errors import *

class RpcRequest:

    def __init__(self, json):
        self._json = json

    @property
    def get_method(self):

        try:
            value = self._json[RpcKeys.method]
        except KeyError as key:
            raise RPCException(message='error =>' + key.__str__() + '<= not found', code=INVALID_PARAMS)

        return value

    @property
    def get_params(self):

        try:
            value = self._json[RpcKeys.params]
        except KeyError as key:
            raise RPCException(message='error =>' + key.__str__() + '<= not found', code=INVALID_PARAMS)

        return value

    @property
    def get_id(self):

        try:
            value = self._json[RpcKeys.id]
        except KeyError as key:
            raise RPCException(message='error =>' + key.__str__() + '<= not found', code=INVALID_PARAMS)

        return value

    @property
    def get_version(self):

        try:
            value = self._json[RpcKeys.jsonrpc]
        except KeyError as key:
            raise RPCException(message='error =>' + key.__str__() + '<= not found', code=INVALID_PARAMS)

        return value

    def  try_get_value_from_params(self, key, type_value):

        try:
            value = self.get_params[key]

        except RPCException as ex:
            raise

        except KeyError:
            raise RPCException(message='error =>' + key + '<= not found', code=INVALID_PARAMS)

        if type(value) != type_value:
            raise RPCException(message='error =>' + key + '<= failed type', code=INVALID_PARAMS)

        return value
