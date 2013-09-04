from django.conf.urls.defaults import patterns, include, url

from csf.recherche.autocomplete_light_registry import *
import autocomplete_light

autocomplete_light.autodiscover()

urlpatterns += patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)
