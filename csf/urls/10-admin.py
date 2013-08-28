from django.conf.urls.defaults import patterns, include, \
        handler500, handler404, url
from django.contrib import admin

admin.autodiscover()

handler404
handler500 # Pyflakes

urlpatterns = patterns('',
    # admin
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login', 'django.contrib.auth.views.login'),
    (r'^accounts/logout', 'django.contrib.auth.views.logout'),
)
