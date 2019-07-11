from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http.request import HttpRequest
import logging


logger = logging.getLogger('django')

class RootView(APIView):

    def get(self, request):

        logger.debug(request.META)
        return Response()