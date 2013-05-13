from django import forms
from django.utils.functional import curry
from django.utils.encoding import force_unicode
from django.forms.widgets import HiddenInput
from django.forms.models import BaseModelFormSet
from .models import (
    Discipline,
    Niveau,
    TypeUrls,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    )


# Formulaires pour interface publique
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
