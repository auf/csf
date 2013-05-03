# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

import auf.django.references.models as ref

from csf.formulaire.models import Discipline, Niveau

@login_required
def home(request):
    c = {
        'pays': ref.Pays.objects.filter(code__in=('BE','CA','FR')),
        'niveaux': Niveau.objects.all(), 
        'disciplines': Discipline.objects.all(),
    }
    return render(request, 'portail/home.html', c)

@login_required
def pays_detail(request, id):
    c = {
        'pays': get_object_or_404(ref.Pays, id=id,),
    }
    return render(request, 'portail/pays_detail.html', c)

@login_required
def niveau_detail(request, id):
    c = {
        'niveau': get_object_or_404(Niveau, id=id,),
    }
    return render(request, 'portail/niveau_detail.html', c)
    
@login_required
def discipline_detail(request, id):
    c = {
        'discipline': get_object_or_404(Discipline, id=id,),
    }
    return render(request, 'portail/discipline_detail.html', c)


