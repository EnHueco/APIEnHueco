__author__ = 'Diego'

import views
from django.conf.urls import patterns, include, url

urlpatterns = [

    url(r'^testing/$', views.GapsViewSet.as_view({'get': 'list'})),

]
