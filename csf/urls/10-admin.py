from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

admin.autodiscover()

handler404
handler500 # Pyflakes

urlpatterns = patterns('',
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
