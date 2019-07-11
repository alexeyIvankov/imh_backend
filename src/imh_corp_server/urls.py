"""imh_corp_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from authorization.api.auth_api_view_root import  authorization_rpc_root
from django.views.generic import RedirectView
from social_network.views import YammerAuthView
from social_network.api.social_network_api_view_root import social_network_rpc_root
from imh_corp_server.settings import *


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'authorization/rpc/$', authorization_rpc_root),
    url(r'social_network/rpc/$', social_network_rpc_root),
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^' + SOCIAL_NETWORK['yammer']['redirect_url'], YammerAuthView.as_view()),
]
