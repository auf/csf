from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from csf.formulaire.models import OffreFormation

# must be registered before it can used
import autocomplete_light_registry

from forms import SearchForm
from filters import OffreFormationFilter


class FormationPlugin(CMSPluginBase):
    name = _("Formation search plugin")
    render_template = "formulaire/_search.html"
    admin_preview = True
    module = _("Formation")

    def render(self, context, instance, placeholder):
        context = super(FormationPlugin, self).render(context, instance, placeholder)
        context['form'] = SearchForm()
        context['filter'] = OffreFormationFilter({}, queryset=OffreFormation.catalogue.all())

        return context

plugin_pool.register_plugin(FormationPlugin)


class FormationListPlugin(CMSPluginBase):
    name = _("Formation list plugin")
    render_template = "formulaire/_list.html"
    admin_preview = True
    module = _("Formation")

    def render(self, context, instance, placeholder):
        context = super(FormationListPlugin, self).render(context, instance, placeholder)
        context['pays'] = set(OffreFormation.catalogue.values_list('etablissement__etablissement__pays__code',
                                                             'etablissement__etablissement__pays__nom').distinct())
        context['niveau'] = set(OffreFormation.catalogue.values_list('niveau__pk', 'niveau__display_name').distinct())
        context['discipline'] = set(OffreFormation.catalogue.values_list('discipline__pk', 'discipline__display_name').distinct())

        return context

plugin_pool.register_plugin(FormationListPlugin)

class PaysListPlugin(CMSPluginBase):
    name = _("Pays list plugin")
    render_template = "formulaire/_pays.html"
    admin_preview = True
    module = _("Formation")

    def render(self, context, instance, placeholder):
        context = super(PaysListPlugin, self).render(context, instance, placeholder)
        pays = set(OffreFormation.catalogue.values_list('etablissement__etablissement__pays__code',
                                                  'etablissement__etablissement__pays__nom').distinct())

        context['pays'] = {}
        for code, name in pays:
            context['pays'][name] = \
                 set(OffreFormation.catalogue.filter(etablissement__etablissement__pays__code=code)\
                 .values_list('etablissement__etablissement__pk', 'etablissement__etablissement__nom'))

        return context

plugin_pool.register_plugin(PaysListPlugin)
