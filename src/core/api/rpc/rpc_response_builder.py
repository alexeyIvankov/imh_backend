from core.api.rpc.rpc_response import Error,Success,Response


class RpcResponseBuilder:

    @classmethod
    def build_from_exception(self, exception:Exception):

        error = Error()
        error.message = exception.message
        error.code = exception.code

        response = Response()
        response.error = error
        response.success = None

        return response

    @classmethod
    def build_from_error(self, message: str, code=None):
        error = Error()
        error.message = message
        error.code = code

        response = Response()
        response.error = error
        response.success = None

        return response

    @classmethod
    def build_from_success(self, data:object):
        success = Success()
        success.data = data

        response = Response()
        response.error = None
        response.success = success

        return response

