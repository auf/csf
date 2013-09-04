from django.views.generic import ListView, DetailView, TemplateView

from csf.formulaire.models import OffreFormation

from forms import SearchForm
from filters import OffreFormationFilter

class SearchView(TemplateView):
    template_name = "formulaire/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['filter'] = OffreFormationFilter(self.request.GET, queryset=OffreFormation.objects.all())
        context['pays'] = set(OffreFormation.objects.values_list('etablissement__etablissement__pays__code',
                                                             'etablissement__etablissement__pays__nom').distinct())
        context['niveau'] = set(OffreFormation.objects.values_list('niveau__pk', 'niveau__display_name').distinct())
        context['discipline'] = set(OffreFormation.objects.values_list('discipline__pk', 'discipline__display_name').distinct())

            
        return context

class EtabliListView(ListView):
    model = OffreFormation

    def get_template_names(self):
        return 'formulaire/discipline.html'

    def get_queryset(self):
        return OffreFormationFilter(self.request.GET, queryset=OffreFormation.objects.all())

class EtabliDetailView(DetailView):
    model = OffreFormation
    template_name = "formulaire/etabli.html"

    def get_context_data(self, **kwargs):
        context = super(EtabliDetailView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['filter'] = OffreFormationFilter(self.request.GET, queryset=OffreFormation.objects.all())

        context['pays_list'] = \
            set(OffreFormation.objects.values_list('etablissement__etablissement__pays__code',
                  'etablissement__etablissement__pays__nom').distinct())
        context['object'].dans_le_pays = \
              OffreFormation.objects.filter(etablissement__etablissement__pays=\
                                            context['object'].etablissement.etablissement.pays)\
                .values_list('etablissement__etablissement__pk', 'etablissement__etablissement__nom')

        return context
