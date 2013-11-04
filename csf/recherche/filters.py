import django_filters

from csf.formulaire.models import OffreFormation


class OffreFormationFilter(django_filters.FilterSet):
    class Meta:
        model = OffreFormation
        fields = ['etablissement__etablissement__pays',
                  'discipline',
                  'niveau',
        ]

    def __init__(self, *args, **kwargs):
        super(OffreFormationFilter,self).__init__(*args, **kwargs)
        self.filters['discipline'].extra['empty_label'] = 'Discipline'
        self.filters['niveau'].extra['empty_label'] = 'Niveau'
        self.filters['etablissement__etablissement__pays'].extra['empty_label'] = 'Pays'

        self.filters['etablissement__etablissement__pays'].extra['queryset'] = \
              self.filters['etablissement__etablissement__pays'].extra['queryset'].filter(code__in=
              OffreFormation.catalogue.values_list('etablissement__etablissement__pays__code')).distinct()
