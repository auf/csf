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
        self.filters['etablissement__etablissement__pays'].queryset = OffreFormation.objects.values('etablissement__etablissement__pays')
