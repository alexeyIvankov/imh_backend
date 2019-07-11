from core.api.rpc.rpc_keys import RpcKeys
from rest_framework.parsers import JSONParser
from core.api.rpc.rpc_request import RpcRequest
from core.api.rpc.rpc_exception import RPCException
from core.api.rpc.rpc_code_errors import *


class RpcRequestParser:

    def __init__(self, parse_data):
        self.request_data = parse_data

    def try_parse(self):

        if self.request_data is None:
            raise RPCException(message='request data not found', code=REQUEST_DATA_NOT_FOUND)

        json = JSONParser().parse(self.request_data)
        if json is None:
            raise RPCException(message='json serialized failed', code=JSON_SERIALIZED_FAILED)

        try:
            json[RpcKeys.method]
        except KeyError:
            raise RPCException(message='method not found', code=METHOD_NOT_FOUND)

        return RpcRequest(json)
