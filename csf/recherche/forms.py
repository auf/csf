# -*- coding: utf-8 -*-

from django import forms

from django.utils.translation import ugettext_lazy as _

import autocomplete_light


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=autocomplete_light.TextWidget(
            'SearchAutocomplete',
            autocomplete_js_attributes={
                'placeholder': _('Recherche interactive'),
                'minimum_characters': 3, }
            )
        )
