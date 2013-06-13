# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from csf.formulaire.models import EtablissementEligible

import auf.django.references.models as ref

from csf.formulaire.models import Discipline, Niveau, OffreFormation

@login_required
@staff_member_required
def home(request):
    if not request.user.is_superuser :
        raise PermissionDenied()
        
    etablissements = EtablissementEligible.objects.all().select_related(
        'etablissement',
        'user',
        'offres_formation'
        )

    c = {
        'etablissements':etablissements
    }
    return render(request, 'gestion/home.html', c)
