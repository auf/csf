from django.conf.urls import patterns

from views import SearchView, EtabliListView, EtabliDetailView

urlpatterns = patterns('',
#    (r'^recherche/$', SearchView.as_view()),
    (r'^$', EtabliListView.as_view()),
    (r'^(?P<pk>\d+)/$', EtabliDetailView.as_view()),
)


