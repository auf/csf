# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.admin import SimpleListFilter
from auf.django.auth_token.admin import TokenUserAdmin
from django.conf import settings
from auf.django.auth_token.models import ALLOW_UNSECURED_TOKEN_AUTH
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
    link = 'http%s://%s%s?auth_token=%s' % (
        (''
         if (settings.DEBUG and ALLOW_UNSECURED_TOKEN_AUTH)
         else 's'),
        Site.objects.get_current().domain,
        reverse('csf.formulaire.views.offre_form',
                kwargs={'id': obj.etablissement_eligible.id,},
                ),
        obj.auf_auth_token.value,
        )
    return mark_safe('<a href="%(link)s">%(link)s</a>' % {'link': link})
show_link.short_description = _(u'Lien')
show_link.allow_tags = True


class IsEtablissementFilter(SimpleListFilter):
    title = 'type'
    parameter_name = 'is_etab'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Etablissement'),
            ('no', 'Utilisateur'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'no':
            return queryset.filter(
                etablissement_eligible__id__isnull=True)

        if self.value() == 'yes':
            return queryset.exclude(
                etablissement_eligible__id__isnull=True)


class UserAdmin(TokenUserAdmin):

    list_display = TokenUserAdmin.list_display + [show_link]
    inlines = TokenUserAdmin.inlines + [EtablissementEligibleInline]
    list_filter = list(TokenUserAdmin.list_filter) + [IsEtablissementFilter]


class OrderedAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'ordering']


admin.site.unregister(User)
admin.site.register(Discipline, OrderedAdmin)
admin.site.register(Niveau, OrderedAdmin)
admin.site.register(TypeUrls, OrderedAdmin)
admin.site.register(User, UserAdmin)
