# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

import auf.django.references.models as ref

from csf.formulaire.models import Discipline, Niveau, OffreFormation

@login_required
def home(request):
    if not request.user.is_superuser :
        raise PermissionDenied()
        
    etablissements = ref.Etablissement.objects.select_related().filter(
        actif=True,
        membre=True,
        qualite='ESR',
        pays__code__in=('BE','CA','FR'),        
    )
    
    c = {
        'etablissements':etablissements,
    }
    return render(request, 'gestion/home.html', c)
