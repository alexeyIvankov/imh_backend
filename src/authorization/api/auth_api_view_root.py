from rest_framework.decorators import api_view
from authorization.api.controllers.auth import AuthController
from core.api.rpc.rpc_response_builder import RpcResponseBuilder
from core.api.rpc.rpc_request_parser import RpcRequestParser
from core.api.rpc.rpc_exception import RPCException
from .supported_methods import  *
from core.api.rpc.rpc_code_errors import *
import inject

authController = inject.instance(AuthController)

@api_view(['GET', 'POST'])
def authorization_rpc_root(request):
    parser = RpcRequestParser(request)

    try:
        rpc_request = parser.try_parse()
        method = rpc_request.get_method
    except RPCException as ex:
        return RpcResponseBuilder.build_from_exception(exception=ex).json()

    if method == AUTHORIZATION_METHOD:
        return authController.authorization(rpc_request)
    elif method == SEND_SMS_METHOD:
        return authController.send_sms(rpc_request)
    else:
        return RpcResponseBuilder.build_from_exception(
            exception=RPCException(message='method not found', code=METHOD_NOT_FOUND)).json()



