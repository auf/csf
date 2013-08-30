from django.conf.urls.defaults import patterns, include, url

import autocomplete_light

autocomplete_light.autodiscover()

urlpatterns += patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
)
