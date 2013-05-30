# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'csf.gestion.views',
    url(r'^$', 'home', name='gestion_home'),
)
