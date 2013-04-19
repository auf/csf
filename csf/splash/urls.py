# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns(
    'csf.splash.views',
    url(r'^$', 'home', name='home'),
)
