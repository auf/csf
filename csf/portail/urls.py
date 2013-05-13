# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns(
    'csf.portail.views',
    url(r'^$', 'home', name='portail_home'),
    #url(r'^pays/(?P<code>\W{2})$', 'pays_detail', name='portail_pays_detail'),
    url(r'^pays/(?P<id>\d+)$', 'pays_detail', name='portail_pays_detail'),
    url(r'^niveau/(?P<id>\d+)$', 'niveau_detail', name='portail_niveau_detail'),
    url(r'^discipline/(?P<id>\d+)$', 'discipline_detail', name='portail_discipline_detail'),
)
