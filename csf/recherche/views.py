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
        context['pays'] = OffreFormation.objects.values_list('etablissement__etablissement__pays__code',
                                                             'etablissement__etablissement__pays__nom').distinct()
        context['niveau'] = OffreFormation.objects.values_list('niveau__pk', 'niveau__display_name').distinct()
        context['discipline'] = OffreFormation.objects.values_list('discipline__pk', 'discipline__display_name').distinct()

            
        return context

class ListView(ListView):
    model = OffreFormation

    def get_template_names(self):
        params = {k:v for k,v in self.request.GET.iteritems() if self.request.GET[k] != ''}

        if params.keys() == ['etablissement__etablissement__pays']:
            return 'formulaire/pays.html'
        elif params.keys() == ['discipline']:
            return 'formulaire/discipline.html'
        elif params.keys() == ['etablissement']:
            return 'formulaire/etablissement.html'
        else:
            return 'formulaire/list.html'

    def get_queryset(self):
        return OffreFormationFilter(self.request.GET, queryset=OffreFormation.objects.all())
