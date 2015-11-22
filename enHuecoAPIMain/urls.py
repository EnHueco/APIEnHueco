from django.conf.urls import patterns, include, url
from django.contrib import admin
from enHuecoAPIMain import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'enHuecoAPIMain.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('core.urls')),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, }),

    url(r'^', include('core.urls')),
)
