# -*- encoding: utf-8 -*-

import itertools
from django.template import RequestContext
from django.contrib import messages
from django.forms.models import (
    inlineformset_factory,
    modelformset_factory,
    )
from django.shortcuts import render_to_response, get_object_or_404
from auf.django.references import models as ref
from .models import (
    Discipline,
    Niveau,
    TypeUrls,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    EtablissementEligible,
    )
from .forms import (
    DraftOffreFormationPublicForm,
    DraftURLEtablissementPublicForm,
    DraftOffreFormationFormSet,
    DraftURLEtablissementFormSet,
    OffreFormationForm,
    URLEtablissementForm,
    )
from django.utils.translation import ugettext as _


def offre_form(request, id):
    etablissement = get_object_or_404(
        EtablissementEligible,
        id=id,
        )

    niveaux = Niveau.objects.all()
    disciplines = Discipline.objects.all()


    ### Create default content if it doesn't exist for this user:

    # First create default URLS

    due_qs = DraftURLEtablissement.objects.filter(
        etablissement=etablissement)
    p_due_qs = URLEtablissement.objects.filter(
        etablissement=etablissement)

    missing = TypeUrls.objects.exclude(
        id__in=due_qs.values_list(
            'type__id', flat=True))
    p_missing = TypeUrls.objects.exclude(
        id__in=due_qs.values_list(
            'type__id', flat=True))


    new_urls = [
        DraftURLEtablissement(
            type=x,
            etablissement=etablissement,
            )
        for x in missing
        ]
    DraftURLEtablissement.objects.bulk_create(new_urls)

    new_p_urls = [
        URLEtablissement(
            type=x,
            etablissement=etablissement,
            )
        for x in p_missing
        ]
    URLEtablissement.objects.bulk_create(new_urls)
    
    # Then create default Offres

    dof_qs = DraftOffreFormation.objects.filter(
        etablissement=etablissement)
    p_dof_qs = DraftOffreFormation.objects.filter(
        etablissement=etablissement)

    rows = set(itertools.product(
        Discipline.objects.all().values_list('id', flat=True),
        Niveau.objects.all().values_list('id', flat=True),
        ))
    current_products = set(dof_qs.values_list('discipline', 'niveau'))
    missing = rows.difference(current_products)
    p_current_products = set(p_dof_qs.values_list('discipline', 'niveau'))
    p_missing = rows.difference(p_current_products)

    new_offres = [
        DraftOffreFormation(
            discipline_id=x[0],
            niveau_id=x[1],
            etablissement_id=etablissement.id,
            )
        for x in missing
        ]
    DraftOffreFormation.objects.bulk_create(new_offres)
    p_new_offres = [
        OffreFormation(
            discipline_id=x[0],
            niveau_id=x[1],
            etablissement_id=etablissement.id,
            )
        for x in p_missing
        ]
    OffreFormation.objects.bulk_create(p_new_offres)


    ### Create formsets

    due_fs = modelformset_factory(
        model=DraftURLEtablissement,
        form=DraftURLEtablissementPublicForm,
        formset=DraftURLEtablissementFormSet,
        extra=0,
        )

    p_due_fs = modelformset_factory(
        model=URLEtablissement,
        form=URLEtablissementForm,
        extra=0,
        )

    dof_fs = modelformset_factory(
        model=DraftOffreFormation,
        form=DraftOffreFormationPublicForm,
        formset=DraftOffreFormationFormSet,
        extra=0,
        )

    p_dof_fs = modelformset_factory(
        model=OffreFormation,
        form=OffreFormationForm,
        extra=0,
        )


    ### Get / Post logic here.

    if request.method == 'GET':
        due = due_fs(queryset=due_qs)
        dof = dof_fs(queryset=dof_qs)
    elif (request.POST.get('publish', '') == 'doit'):

        for draft_offre in dof_qs:
            offre, nothing = OffreFormation.objects.get_or_create(
                etablissement=etablissement,
                niveau=draft_offre.niveau,
                discipline=draft_offre.discipline,
                )
            offre.offert = draft_offre.offert
            offre.save()

        for draft_url in due_qs:
            url, nothing = URLEtablissement.objects.get_or_create(
                etablissement=etablissement,
                type=draft_url.type,
                )
            url.url = draft_url.url
            url.save()

        etablissement.participant = True
        etablissement.save()

        msg = _(u'Vos informations ont été publiées.')
        messages.success(
            request,
            msg,
            )

        due = due_fs(queryset=due_qs)
        dof = dof_fs(queryset=dof_qs)

    elif (request.POST.get('take-down', '') == 'doit'):
        etablissement.participant = False
        etablissement.save()

        msg = _(u'Votre publication a été enlevée.')
        messages.warning(
            request,
            msg,
            )
        due = due_fs(queryset=due_qs)
        dof = dof_fs(queryset=dof_qs)

    elif request.method == 'POST':
        due = due_fs(request.POST)
        dof = dof_fs(request.POST)
    
        if due.is_valid() and dof.is_valid():
            due.save()
            dof.save()
            msg = _(u'Vos changements ont été sauvegardés.')
            messages.success(
                request,
                msg,
                )
        else:
            msg = _(u'Des erreurs se sont produites, veuillez vérifier'
                    ' les erreurs ci-dessous.')
            messages.error(
                request,
                msg,
                )
               
    ctx = {
        'due': due,
        'dof': dof,
        'p_due': p_due_fs(
            queryset=etablissement.urls.all()),
        'p_dof': p_dof_fs(
            queryset=etablissement.offres_formation.all()),
        'typeurls': TypeUrls.objects.all(),
        'niveaux': niveaux,
        'dof_column_count': niveaux.count(),
        'etablissement': etablissement,
        }

    return render_to_response(
        'formulaire/offre_form.html',
        ctx,
        context_instance=RequestContext(request, {}),
        )
