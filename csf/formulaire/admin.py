from django.contrib import admin
from django.contrib.auth.models import User
from auf.django.auth_token.admin import TokenUserAdmin
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


class UserAdmin(TokenUserAdmin):
    inlines = TokenUserAdmin.inlines + [EtablissementEligibleInline]


class OrderedAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'ordering']


admin.site.unregister(User)
admin.site.register(Discipline, OrderedAdmin)
admin.site.register(Niveau, OrderedAdmin)
admin.site.register(TypeUrls, OrderedAdmin)
admin.site.register(User, UserAdmin)
