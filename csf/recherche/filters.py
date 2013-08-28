import django_filters

from csf.formulaire.models import OffreFormation


class OffreFormationFilter(django_filters.FilterSet):
    class Meta:
        model = OffreFormation
        fields = ['etablissement__etablissement__pays',
                  'discipline',
                  'niveau',
        ]
