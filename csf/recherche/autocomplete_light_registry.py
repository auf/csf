# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils.translation import ugettext as _

from csf.formulaire.models import OffreFormation

import autocomplete_light

class SearchAutocomplete(autocomplete_light.AutocompleteBase):

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        results = {}
        results['offre'] = OffreFormation.catalogue.filter(
                                    Q(etablissement__etablissement__nom__icontains=q) |
                                    Q(discipline__display_name__icontains=q) |
                                    Q(niveau__display_name__icontains=q)
                                   ).distinct()[:10]

        return results

    def autocomplete_html(self):
        html = []

        choice_html_format = """
<span class="div" style="text-align: left;">
  <a class="blue" href="/recherche/%s/">
   %s  
  </a>
</span>"""

        choice = self.choices_for_request()

        for item in choice['offre']:
            html.append(choice_html_format % (item.etablissement.etablissement.id,
					      unicode(item).split(':')[0]))

        if not html:
            html = self.empty_html_format % _(u'aucun résultat').capitalize()

        return self.autocomplete_html_format % ''.join(html)

autocomplete_light.register(SearchAutocomplete)

