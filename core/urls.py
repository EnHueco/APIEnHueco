__author__ = 'Diego'

from core import views
from django.conf.urls import patterns, include, url


urlpatterns = [

# AUTHENTICATION
    url(r'^auth/$', views.Authenticate.as_view()),
# ME
    url(r'^me', views.UserDetail.as_view(), name='show-me'),
# SCHEDULES
    url(r'^schedule/$', views.GapsList.as_view(), name='show-schedule'),
###    url(r'^schedule/update/$', views.UpdateMySchedule.as_view(), name='update-schedule'),
###    url(r'^schedule/(?P<friendPK>[a-z]+(\.)?[a-z]+[0-9]*)/cross/$', views.CrossFriendSchedule.as_view(), name='show-cross-schedule-friend'),
###    url(r'^schedule/(?P<friendPK>[a-z]+(\.)?[a-z]+[0-9]*)/', views.ShowFriendSchedule.as_view(), name='show-friend-schedule'),
###    url(r'^schedule/day/update/$', views.UpdateMyScheduleDay.as_view(), name='update-schedule-day'),
# FRIEND REQUESTS
    url(r'^requests/sent/$', views.SentFriendRequestList.as_view(), name='sent-friend-requests-list'),
    url(r'^requests/received/$', views.ReceivedFriendRequestsList.as_view(), name='received-friend-requests-list'),
# FRIENDS
    url(r'^friends/$', views.FriendList.as_view(), name='friend-list'),
    url(r'^friends/(?P<fpk>[a-z]+(\.)?[a-z]+[0-9]*)/$', views.FriendDetail.as_view(), name='friend-detail'),
]

