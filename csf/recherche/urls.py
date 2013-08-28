from django.conf.urls import patterns

from views import SearchView, ListView, DetailView

urlpatterns = patterns('',
#    (r'^recherche/$', SearchView.as_view()),
    (r'^$', ListView.as_view()),
    (r'^(?P<pk>\d+)/$', DetailView.as_view()),
)


