# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, TemplateView

from auf.django.references import models as ref

from csf.formulaire.models import OffreFormation

from forms import SearchForm
from filters import OffreFormationFilter

class SearchView(TemplateView):
    template_name = "formulaire/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        context['filter'] = OffreFormationFilter(self.request.GET,
                queryset=OffreFormation.catalogue.all())
        context['pays'] = set(OffreFormation.catalogue.values_list('etablissement__etablissement__pays__code',
                                                             'etablissement__etablissement__pays__nom').distinct())
        context['niveau'] = set(OffreFormation.catalogue.values_list('niveau__pk', 'niveau__display_name').distinct())
        context['discipline'] = set(OffreFormation.catalogue.values_list('discipline__pk', 'discipline__display_name').distinct())

            
        return context


def _check_niveaux(new_object_list, obj):
    for new_obj in new_object_list:
        if new_obj['discipline'] == obj.discipline and \
           new_obj['pk'] == obj.etablissement.etablissement.pk:

            new_obj['niveaux'].append(obj.niveau)
            return False

    return True

class EtabliListView(ListView):
    model = OffreFormation

    def get_template_names(self):
        return 'formulaire/discipline.html'

    def get_context_data(self, **kwargs):
        context = super(EtabliListView, self).get_context_data(**kwargs)

        context['form'] = SearchForm()
        context['filter'] = context['object_list']

        new_object_list = []
        for obj in context['object_list'].qs:

            need_to_add = _check_niveaux(new_object_list, obj)        
            if need_to_add:
                new_object_list.append(
                    {
                     'discipline': obj.discipline, 
                      'pk': obj.etablissement.etablissement.pk,
                      'nom': obj.etablissement.etablissement.nom,
                      'pays': obj.etablissement.etablissement.pays.nom,
                      'niveaux': [obj.niveau],
		      'images': obj.etablissement.images,
                      }
                 )

        context['object_list'] = new_object_list

        return context

    def get_queryset(self):
        return OffreFormationFilter(self.request.GET,
                queryset=OffreFormation.catalogue\
                        .all()\
                        .select_related(
                            'niveau',
                            'discipline',
                            'etablissement__etablissement',
                            'etablissement__etablissement__pays',
                            'etablissement__images')\
                        .order_by('discipline__display_name', 'niveau__ordering')
                        )


class EtabliDetailView(DetailView):
    # id dans l'url correspond à ref.etablissement mais n'est pas utilisé dans la vue
    model = ref.Etablissement 
    template_name = "formulaire/etabli.html"

    def get_context_data(self, **kwargs):
        context = super(EtabliDetailView, self).get_context_data(**kwargs)


        pk = self.kwargs.get(self.pk_url_kwarg, None)

	offre = OffreFormation.catalogue\
                .filter(etablissement__etablissement__pk=pk)\
                .select_related(
                        'etablissement',
                        'etablissement__images')[0]
	context['images'] = offre.etablissement.images
	context['etabli'] = offre.etablissement.etablissement

        context['form'] = SearchForm()
        context['filter'] = OffreFormationFilter(self.request.GET, queryset=OffreFormation.catalogue.all())

        context['disciplines'] = [{'discipline': c.discipline, 'niveau': c.niveau} for c in OffreFormation.catalogue.filter(etablissement__etablissement__pk=context['etabli'].pk)]

        context['etabli'].dans_le_pays = \
            set(OffreFormation.catalogue.filter(etablissement__etablissement__pays__code=\
                                             context['etabli'].pays.code)\
                .values_list('etablissement__etablissement__pk', 'etablissement__etablissement__nom'))
        return context
