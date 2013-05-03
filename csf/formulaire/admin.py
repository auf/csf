from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from auf.django.auth_token.admin import TokenUserAdmin
from django.core.urlresolvers import reverse
from .models import (
    Discipline,
    Niveau,
    TypeUrls,
    EtablissementEligible,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    )
    

class DraftURLEtablissementInline(admin.StackedInline):
    model = DraftURLEtablissement


class DraftOffreFormationInline(admin.StackedInline):
    model = DraftOffreFormation


class URLEtablissementInline(admin.StackedInline):
    model = URLEtablissement


class OffreFormationInline(admin.StackedInline):
    model = OffreFormation


class EtablissementEligibleInline(admin.StackedInline):
    model = EtablissementEligible


def show_link(obj):
    link = 'http://%s%s?auth_token=%s' % (
        Site.objects.get_current().domain,
        reverse('csf.formulaire.views.offre_form',
                kwargs={'id': obj.etablissement_eligible.id,},
                ),
        obj.auf_auth_token.value,
        )
    return mark_safe('<a href="%(link)s">%(link)s</a>' % {'link': link})
show_link.short_description = _(u'Lien')
show_link.allow_tags = True

class UserAdmin(TokenUserAdmin):

    list_display = TokenUserAdmin.list_display + [show_link]
    inlines = TokenUserAdmin.inlines + [EtablissementEligibleInline]


class OrderedAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'ordering']


admin.site.unregister(User)
admin.site.register(Discipline, OrderedAdmin)
admin.site.register(Niveau, OrderedAdmin)
admin.site.register(TypeUrls, OrderedAdmin)
admin.site.register(User, UserAdmin)
