
urlpatterns += i18n_patterns('',
    url(r'^recherche/', include('csf.recherche.urls')),
    url(r'^api/pong/', include('auf.django.pong.urls')),
)

