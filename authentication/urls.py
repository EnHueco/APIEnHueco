__author__ = 'Diego'

from authentication import views
from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^', views.Authenticate.as_view()),
#    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

