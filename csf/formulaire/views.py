# -*- encoding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import Http404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import (
    inlineformset_factory,
    modelformset_factory,
    )
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import PermissionDenied
from auf.django.references import models as ref
from .models import (
    Discipline,
    ContactInfo,
    Niveau,
    TypeUrls,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    EtablissementEligible,
    )
from .forms import (
    EtabEligibleForm,
    ContactInfoForm,
    DraftOffreFormationPublicForm,
    DraftURLEtablissementPublicForm,
    DraftOffreFormationFormSet,
    DraftURLEtablissementFormSet,
    OffreFormationForm,
    URLEtablissementForm,
    )
from django.utils.translation import ugettext as _



def check_etablissement(fun):
    def inner(request, id):
        etablissement = get_object_or_404(
            EtablissementEligible,
            id=id,
            )

        # Quick permission check.
        request.can_edit_etablissement = False
        if not request.user.is_staff:
            try:
                etab_eligible = request.user.etablissement_eligible
            except EtablissementEligible.DoesNotExist:
                raise PermissionDenied()
            else:
                if (etab_eligible.etablissement.id !=
                    etablissement.etablissement.id):
                    raise PermissionDenied()
                else:
                    request.can_edit_etablissement = True
        else:
            request.can_edit_etablissement = True

        ### Create default URLs and Offres if any are missing.
        DraftURLEtablissement.create_missing(etablissement)
        URLEtablissement.create_missing(etablissement)
        DraftOffreFormation.create_missing(etablissement)
        OffreFormation.create_missing(etablissement)
        ContactInfo.objects.get_or_create(etablissement=etablissement)

        return fun(request, etablissement)
    return inner


@check_etablissement
@login_required
def preview(request, etablissement):
    if etablissement.participant in (None, False):
        raise Http404()

    niveaux = Niveau.objects.all()

    ctx = {
        'etablissement': etablissement,
        'niveaux': niveaux,
        'offre_column_count': niveaux.count(),
        }

    return render_to_response(
        'formulaire/offre_preview.html',
        ctx,
        context_instance=RequestContext(request, {}),
        )


@check_etablissement
@login_required
def offre_form(request, etablissement):
    if etablissement.participant == None:
        etablissement.participant = True
        etablissement.save()

    niveaux = Niveau.objects.all()
    disciplines = Discipline.objects.all()

    ### Get Querysets
    due_qs = DraftURLEtablissement.objects.filter(
        etablissement=etablissement)
    dof_qs = DraftOffreFormation.objects.filter(
        etablissement=etablissement)

    ### Create formsets and forms
    etab_f = EtabEligibleForm(instance=etablissement)

    contact_f = ContactInfoForm(instance=etablissement.contact_info)
    due_fs = modelformset_factory(
        model=DraftURLEtablissement,
        form=DraftURLEtablissementPublicForm,
        formset=DraftURLEtablissementFormSet,
        extra=0,
        )
    dof_fs = modelformset_factory(
        model=DraftOffreFormation,
        form=DraftOffreFormationPublicForm,
        formset=DraftOffreFormationFormSet,
        extra=0,
        )

    ### Get / Post logic here.
    due = due_fs(queryset=due_qs)
    dof = dof_fs(queryset=dof_qs)

    if (request.POST.get('change-participate', '') in
          ('true', 'false')):
        chp = request.POST.get('change-participate')
        new_val = True if chp == 'true' else False
        if etablissement.participant != new_val:
            etablissement.participant = new_val
            etablissement.save()

    elif (request.POST.get('take-down', '') == 'doit'):
        etablissement.participant = False
        etablissement.save()

        msg = _(u'Votre publication a été enlevée.')
        messages.warning(
            request,
            msg,
            )

    elif request.method == 'POST':
        due = due_fs(request.POST)
        dof = dof_fs(request.POST)
        contact_f = ContactInfoForm(
            request.POST,
            instance=etablissement.contact_info,
            )
        etab_f = EtabEligibleForm(
            request.POST,
            request.FILES,
            instance=etablissement,
            )
    
        if (due.is_valid()
            and dof.is_valid()
            and etab_f.is_valid()
            and contact_f.is_valid()):
            due.save()
            dof.save()
            etab_f = EtabEligibleForm(instance=etab_f.save())
            contact_f.is_valid()
            msg = _(u'Vos changements ont été sauvegardés.')
            messages.success(
                request,
                msg,
                )
            if request.POST.get('publish_draft', None) == 'true':

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
                # redirect
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
        'typeurls': TypeUrls.objects.all(),
        'niveaux': niveaux,
        'dof_column_count': niveaux.count(),
        'etablissement': etablissement,
        'etab_form': etab_f,
        'contact_form': contact_f,
        }

    return render_to_response(
        'formulaire/offre_form.html',
        ctx,
        context_instance=RequestContext(request, {}),
        )
