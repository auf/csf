# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

handler404
handler500 # Pyflakes

urlpatterns = patterns(
    '',
    # admin
    url(r'^$', include('csf.splash.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^form/(?P<id>\d+)/$',
        'csf.formulaire.views.offre_form',
        name='form_url'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^accounts/logout', 'django.contrib.auth.views.logout'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
        'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT, }),
        )
