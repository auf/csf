# -*- encoding: utf-8 -*-

from django import forms
from django.utils.functional import curry
from django.utils.encoding import force_unicode
from django.forms.widgets import HiddenInput
from django.forms.models import BaseModelFormSet
from django.conf import settings
from .models import (
    Discipline,
    Niveau,
    TypeUrls,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    EtablissementEligible,
    ContactInfo,
    )


FORMULAIRE_IMAGE_MAX_SIZE = getattr(
    settings,
    'FORMULAIRE_IMAGE_MAX_SIZE',
    5000 * 1024,
    )

FORMULAIRE_IMAGE_SIZE_ERROR = getattr(
    settings,
    'FORMULAIRE_IMAGE_SIZE_ERROR',
    "La taille maximum acceptée est de %skB" % (
        FORMULAIRE_IMAGE_MAX_SIZE / 1024),
    )


# Formulaires pour interface publique
class EtabEligibleForm(forms.ModelForm):
    def _clean_img(self, field):
        img = self.cleaned_data.get(field, None)
        if img and img.size > FORMULAIRE_IMAGE_MAX_SIZE:
            raise forms.ValidationError(FORMULAIRE_IMAGE_SIZE_ERROR)
        return img

    def clean_photo(self):
        return self._clean_img('photo')
        
    def clean_logo(self):
        return self._clean_img('logo')

    class Meta:
        fields = [
            'logo', 'photo',
            ]
        model = EtablissementEligible


class ContactInfoForm(forms.ModelForm):
    class Meta:
        exclude = [
            'etablissement',
            ]
        model = ContactInfo


class DraftOffreFormationPublicForm(forms.ModelForm):
    def __init__(self, *a, **kw):
        super(DraftOffreFormationPublicForm,
              self).__init__(*a, **kw)
        self.fields['etablissement'].widget = HiddenInput()
        self.fields['discipline'].widget = HiddenInput()
        self.fields['niveau'].widget = HiddenInput()


class DraftURLEtablissementPublicForm(forms.ModelForm):
    def __init__(self, *a, **kw):
        super(DraftURLEtablissementPublicForm,
              self).__init__(*a, **kw)
        self.fields['etablissement'].widget = HiddenInput()
        self.fields['type'].widget = HiddenInput()


class OffreFormationForm(DraftOffreFormationPublicForm):
    def __init__(self, *a, **kw):
        super(OffreFormationForm,  self).__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs['readonly'] = 'readonly'


class URLEtablissementForm(DraftURLEtablissementPublicForm):
    def __init__(self, *a, **kw):
        super(URLEtablissementForm,  self).__init__(*a, **kw)
        for f in self.fields.values():
            f.widget.attrs['readonly'] = 'readonly'
    
    
class DraftURLEtablissementFormSet(BaseModelFormSet):
    def __init__(self, *a, **kw):
        kw['prefix'] = 'due'
        super(DraftURLEtablissementFormSet, self).__init__(*a, **kw)


class DraftOffreFormationFormSet(BaseModelFormSet):
    def __init__(self, *a, **kw):
        kw['prefix'] = 'dof'
        super(DraftOffreFormationFormSet, self).__init__(*a, **kw)
