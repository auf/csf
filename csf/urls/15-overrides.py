from django.views.generic.base import RedirectView

urlpatterns += patterns(
    '',
    url(r'^\w\w/pied/$', RedirectView.as_view(url='/')),
)
