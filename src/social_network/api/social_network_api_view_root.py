from rest_framework.decorators import api_view
from social_network.api.controllers.social_network_controller import SocialNetworkController
from core.api.rpc.rpc_response_builder import RpcResponseBuilder
from core.api.rpc.rpc_request_parser import RpcRequestParser
from core.api.rpc.rpc_exception import RPCException
from .supported_methods import  *
from core.api.rpc.rpc_code_errors import *
import inject

social_network_controller = inject.instance(SocialNetworkController)


@api_view(['GET', 'POST'])
def social_network_rpc_root(request):

    parser = RpcRequestParser(request)

    try:
        rpc_request = parser.try_parse()
        method = rpc_request.get_method
    except RPCException as ex:
        return RpcResponseBuilder.build_from_exception(exception=ex).json()

    if method == GET_ALL_GROUPS_METHOD:
        return social_network_controller.get_all_groups(rpc_request)
    elif method == GET_ALL_NEWS_METHOD:
        return social_network_controller.get_all_news(rpc_request)
    elif method == GET_NEWS_SELECTED_GROUPS_METHOD:
        return social_network_controller.get_news_selected_groups(rpc_request)
    elif method == GET_NEWS_EXCEPT_GROUPS_METHOD:
        return  social_network_controller.get_news_except_groups(rpc_request)
    elif method == GET_ATTACH_METHOD:
        return social_network_controller.get_attach(rpc_request)
    elif method == GET_IMAGE_METHOD:
        return  social_network_controller.get_image(rpc_request)
    else:
        return RpcResponseBuilder.build_from_exception(exception=RPCException(message='method not found', code=METHOD_NOT_FOUND)).json()
