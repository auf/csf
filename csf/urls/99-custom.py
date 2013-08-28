# -*- encoding: utf-8 -*-

urlpatterns += patterns('',
        
    # interfaces publiques
    url(r'^$', include('csf.splash.urls')),
    url(r'^demo/', include('csf.portail.urls')),
    url(r'^etablissement/(?P<id>\d+)/$',
        'csf.formulaire.views.preview',
        name='etab_preview'),
        
    # interfaces privées : AUF
    url(r'^gestion/', include('csf.gestion.urls')),
    
    
    # interfaces privées : membre
    url(r'^espace/membre/(?P<id>\d+)/$',
        'csf.formulaire.views.offre_form',
        name='form_url'),
        

)
