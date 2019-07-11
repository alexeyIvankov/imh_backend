from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from persons import views


urlpatterns = [
    url(r'^$', views.PersonList.as_view()),
    url(r'^persons//(?P<pk>[a-z]+)$', views.PersonDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
