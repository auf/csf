# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from auf.django.auth_token.admin import TokenUserAdmin, reset_token
from django.conf import settings
from .models import (
    Discipline,
    Niveau,
    TypeUrls,
    EtablissementEligible,
    DraftURLEtablissement,
    DraftOffreFormation,
    URLEtablissement,
    OffreFormation,
    show_edit_link,
    show_link,
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

    list_display = list(DjangoUserAdmin.list_display) + [
        show_edit_link, show_link]
    inlines = TokenUserAdmin.inlines + [EtablissementEligibleInline]
    list_filter = list(TokenUserAdmin.list_filter) + [IsEtablissementFilter]
    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        if 'send_token_by_email' in actions:
            del actions['send_token_by_email']
        return actions


class OrderedAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'ordering']


class TypeUrlsAdmin(OrderedAdmin):
    exclude = ('required',)

class OffreFormationAdmin(admin.ModelAdmin):
    pass

admin.site.register(OffreFormation, OffreFormationAdmin)
admin.site.unregister(User)
admin.site.register(Discipline, OrderedAdmin)
admin.site.register(Niveau, OrderedAdmin)
admin.site.register(TypeUrls, TypeUrlsAdmin)
admin.site.register(User, UserAdmin)
