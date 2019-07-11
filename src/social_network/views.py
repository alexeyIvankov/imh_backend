from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
from social_network.api.controllers.social_network_controller import SocialNetworkController
from social_network.daemons.daemon_latest_news_yammer import DaemonLatestNewsYammer
import inject

class YammerAuthView(APIView):
    social_network_controller = inject.instance(SocialNetworkController)
    yammer_worker = inject.instance(DaemonLatestNewsYammer)

    def get(self, request):

        try:
            code = request.GET['code']
        except KeyError as ex:
            return Response(str(ex))

        try:
            self.social_network_controller.yammer_service.try_set_or_update_authorization(code=code)
        except Exception as ex:
            return Response(str(ex))

        messages.info(request, 'Токены успешно получены!')

        if self.yammer_worker.is_run() == False:
            try:
                self.yammer_worker.try_start()
                messages.info(request, 'Воркер загрузки данных успешно запущен!')
            except Exception as ex:
                messages.info(request, ex)


        return HttpResponseRedirect('/admin/social_network/socialnetworksite/yammer/change/')

# Create your views here.
