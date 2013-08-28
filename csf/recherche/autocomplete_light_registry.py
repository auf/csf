from django.db.models import Q
from django.utils.translation import ugettext as _

from csf.formulaire.models import OffreFormation

import autocomplete_light

class SearchAutocomplete(autocomplete_light.AutocompleteBase):

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        results = {}

        results['offre'] = OffreFormation.objects.filter(
                                    Q(etablissement__etablissement__nom__icontains=q) |
                                    Q(discipline__display_name__icontains=q) |
                                    Q(niveau__display_name__icontains=q)
                                   ).distinct()

        return results

    def autocomplete_html(self):
        html = []

        choice_html_format = u"""
<span class="div">
  <a href="../?etablissement__etablissement__pays=%s&niveau=%s&discipline=%s">
  %s
  </a>
</span>"""

        choice = self.choices_for_request()

        for item in choice['offre']:
            html.append(choice_html_format % (item.etablissement.etablissement.pays.code,
                                              item.niveau.pk,
                                              item.discipline.pk,
                                              str(item).split(':')[0]))

        if not html:
            html = self.empty_html_format % _('no matches found').capitalize()

        return self.autocomplete_html_format % ''.join(html)

autocomplete_light.register(SearchAutocomplete)

