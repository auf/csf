from django import forms

import autocomplete_light

class SearchForm(forms.Form):
    search = forms.CharField(
               widget=autocomplete_light.TextWidget('SearchAutocomplete'))
