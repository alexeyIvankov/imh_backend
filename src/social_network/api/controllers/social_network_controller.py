
from core.api.rpc.rpc_response_builder import RpcResponseBuilder
from authorization.api.services.check_auth_service import CheckAuthService
from core.api.rpc.rpc_exception import RPCException
from social_network.services.db_service import DBServiceSocialNetwork
from social_network.services.yammer_service import YammerService
from django.http import HttpResponse
from enum import Enum
import urllib3
from PIL import Image, _binary
from resizeimage import resizeimage
import io


class NetworkTypes(Enum):
    YAMMER = 'yammer'
    VK = 'vk'
    FACEBOOK = 'facebook'

class SocialNetworkController:


    def __init__(self,
                 yammer_service:YammerService,
                 db_service:DBServiceSocialNetwork,
                 check_auth_service:CheckAuthService):
        self.db_service = db_service
        self.check_auth_service = check_auth_service
        self.yammer_service = yammer_service


    def get_image(self, rpc_request):

        try:
            url = rpc_request.try_get_value_from_params('url', str)
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)

        except Exception as ex:
            return  HttpResponse(ex,status=502)

        try:
            height = rpc_request.try_get_value_from_params('height', int)
            width =  rpc_request.try_get_value_from_params('width', int)
        except:
            height = None
            width = None

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return HttpResponse(ex, status=401)

        if network_type == NetworkTypes.YAMMER.value:

            file_downloader = urllib3.PoolManager()
            download_response = file_downloader.request('GET', url=url, headers={
                "Authorization": "Bearer %s" % self.yammer_service.get_access_token(),
            })

            if download_response.status == 200:
                file_data = download_response.data

                if height != None and width != None:

                    try:
                        image = Image.open(io.BytesIO(file_data))
                    except:
                        image = None

                    if image != None:
                        image = resizeimage.resize_crop(image, [width, height])
                        image_byttes = io.BytesIO()
                        image.save(image_byttes, format='JPEG')
                        file_data = image_byttes.getvalue()

                response = HttpResponse(file_data, content_type='application/file')
                response['Content-Disposition'] = 'attachment; filename=attach'

                return response
            else:
                return HttpResponse('Не удалось загрузить изображение', status=502)
        else:
            return HttpResponse('Тип соц сети не поддерживается', status=502)


    def get_attach(self, rpc_request):
        try:
            url = rpc_request.try_get_value_from_params('url', str)
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)

        except Exception as ex:
            return  HttpResponse(ex,status=502)

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return HttpResponse(ex, status=401)

        if network_type == NetworkTypes.YAMMER.value:

            file_downloader = urllib3.PoolManager()
            download_response = file_downloader.request('GET', url=url, headers={
                "Authorization": "Bearer %s" % self.yammer_service.get_access_token(),
            })

            if download_response.status == 200:
                file_data = download_response.data
                response = HttpResponse(file_data, content_type='application/file')
                response['Content-Disposition'] = 'attachment; filename=attach'

                return response
            else:
                return HttpResponse('Не удалось загрузить файл', status=502)
        else:
            return HttpResponse('Тип соц сети не поддерживается', status=502)


    def get_all_groups(self, rpc_request):
        try:
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)

        except Exception as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()


        if network_type == NetworkTypes.YAMMER.value:
            groups_query_set = self.db_service.gel_all_groups()
            groups_list = []

            for group_db in groups_query_set:
                groups_list.append(group_db.json())

            return RpcResponseBuilder.build_from_success(data={'groups':groups_list}).json()
        else:
            return  RpcResponseBuilder.build_from_error(message='Тип соц сети не поддерживается').json()



    def get_news_selected_groups(self, rpc_request):

        try:
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)
            selected_groups:list = rpc_request.try_get_value_from_params('selected_groups', list)

        except Exception as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        if selected_groups.__len__() == 0:
            return  RpcResponseBuilder.build_from_error(message='list group id is empty').json()

        try:
            start_date = rpc_request.try_get_value_from_params('start_date', int)
        except:
            start_date = None

        try:
            end_date = rpc_request.try_get_value_from_params('end_date', int)
        except:
            end_date = None

        try:
            count = rpc_request.try_get_value_from_params('count', int)
        except:
            count = None

        if network_type == NetworkTypes.YAMMER.value:
            news_query_set = self.db_service.get_news_list_selected_groups(groups_id_list=selected_groups,
                                                                           start_date=start_date,
                                                                           end_date=end_date,
                                                                           count=count)
            news_list = []

            for news_db in news_query_set:
                attaches_query_set = self.db_service.get_all_attaches(news_db=news_db)
                attaches_list_images = []
                attaches_list_files = []

                for attach_db in attaches_query_set:
                    if attach_db.type == 'image':
                        attaches_list_images.append(attach_db.json())
                    else:
                        attaches_list_files.append(attach_db.json())



                news_json = news_db.json()
                news_json['attaches'] = {'images':attaches_list_images,
                                         'files':attaches_list_files}
                news_list.append(news_json)

            return RpcResponseBuilder.build_from_success(data={'news':news_list}).json()

        else:
            return RpcResponseBuilder.build_from_error(message='Тип соц сети не поддерживается').json()



    def get_news_except_groups(self, rpc_request):

        try:
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)
            except_groups:list = rpc_request.try_get_value_from_params('except_groups', list)

        except Exception as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        if except_groups.__len__() == 0:
            return  RpcResponseBuilder.build_from_error(message='list except group id is empty').json()

        try:
            start_date = rpc_request.try_get_value_from_params('start_date', int)
        except:
            start_date = None

        try:
            end_date = rpc_request.try_get_value_from_params('end_date', int)
        except:
            end_date = None

        try:
            count = rpc_request.try_get_value_from_params('count', int)
        except:
            count = None

        if network_type == NetworkTypes.YAMMER.value:
            news_query_set = self.db_service.get_news_list_except_groups(groups_id_list=except_groups,
                                                                         start_date=start_date,
                                                                         end_date=end_date,
                                                                         count=count)
            news_list = []

            for news_db in news_query_set:
                attaches_query_set = self.db_service.get_all_attaches(news_db=news_db)
                attaches_list_images = []
                attaches_list_files = []

                for attach_db in attaches_query_set:
                    if attach_db.type == 'image':
                        attaches_list_images.append(attach_db.json())
                    else:
                        attaches_list_files.append(attach_db.json())



                news_json = news_db.json()
                news_json['attaches'] = {'images':attaches_list_images,
                                         'files':attaches_list_files}
                news_list.append(news_json)

            return RpcResponseBuilder.build_from_success(data={'news':news_list}).json()

        else:
            return RpcResponseBuilder.build_from_error(message='Тип соц сети не поддерживается').json()



    def get_all_news(self, rpc_request):
        try:
            access_token = rpc_request.try_get_value_from_params('access_token', str)
            network_type = rpc_request.try_get_value_from_params('network_type', str)

        except Exception as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        try:
            self.check_auth_service.check_auth(access_token=access_token)
        except RPCException as ex:
            return RpcResponseBuilder.build_from_exception(exception=ex).json()

        try:
            start_date = rpc_request.try_get_value_from_params('start_date', int)
        except:
            start_date = None

        try:
            end_date = rpc_request.try_get_value_from_params('end_date', int)
        except:
            end_date = None

        try:
            count = rpc_request.try_get_value_from_params('count', int)
        except:
            count = None


        if network_type == NetworkTypes.YAMMER.value:
            news_query_set = self.db_service.get_all_news_list(start_date=start_date, end_date=end_date, count=count)
            news_list = []

            for news_db in news_query_set:
                attaches_query_set = self.db_service.get_all_attaches(news_db=news_db)
                attaches_list_images = []
                attaches_list_files = []

                for attach_db in attaches_query_set:
                    if attach_db.type == 'image':
                        attaches_list_images.append(attach_db.json())
                    else:
                        attaches_list_files.append(attach_db.json())



                news_json = news_db.json()
                news_json['attaches'] = {'images':attaches_list_images,
                                         'files':attaches_list_files}
                news_list.append(news_json)

            return RpcResponseBuilder.build_from_success(data={'news':news_list}).json()

        else:
            return RpcResponseBuilder.build_from_error(message='Тип соц сети не поддерживается').json()

