# -*- encoding: utf-8 -*-

import itertools
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from auf.django.references import models as ref
from auf.django.auth_token.models import ALLOW_UNSECURED_TOKEN_AUTH
from django.utils.translation import ugettext_lazy as _


class OrderedModel(models.Model):
    ordering = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        )

    class Meta:
        abstract = True
        ordering = ['ordering']


class Discipline(OrderedModel):
    display_name = models.CharField(
        max_length=255,
        verbose_name="Nom d'affichage",
        )
    def __unicode__(self):
        return self.display_name


class Niveau(OrderedModel):
    display_name = models.CharField(
        max_length=255,
        verbose_name="Nom d'affichage",
        )

    def __unicode__(self):
        return self.display_name

    class Meta:
        ordering = ['ordering']
        verbose_name = _(u'Niveau universitaire')
        verbose_name_plural = _(u'Niveaux universitaires')


class TypeUrls(OrderedModel):
    required = models.BooleanField(
        default=False,
        verbose_name="Obligatoire",
        )
    display_name = models.CharField(
        max_length=255,
        verbose_name="Nom d'affichage",
        )
    help_text = models.CharField(
        max_length=2048,
        blank=True,
        null=True,
        )

    class Meta:
        ordering = ['ordering']
        verbose_name = _(u'Type d\'URL')
        verbose_name_plural = _(u'Types d\'URL')

    def __unicode__(self):
        return self.display_name


def show_edit_link(obj, just_link=False):
    link = 'http%s://%s%s?auth_token=%s' % (
        (''
         if ALLOW_UNSECURED_TOKEN_AUTH
         else 's'),
        Site.objects.get_current().domain,
        reverse('csf.formulaire.views.offre_form',
                kwargs={'id': obj.etablissement_eligible.id,},
                ),
        obj.auf_auth_token.value,
        )
    if just_link:
        return link
    return mark_safe('<a href="%(link)s">%(link)s</a>' % {'link': link})
show_edit_link.short_description = _(u'Lien d\'édition')
show_edit_link.allow_tags = True


def show_link(obj, just_link=False):
    etab_elig = getattr(obj, 'etablissement_eligible', None)
    if not etab_elig or etab_elig.participant in (False, None):
        return None
    link = 'http%s://%s%s?auth_token=%s' % (
        (''
         if ALLOW_UNSECURED_TOKEN_AUTH
         else 's'),
        Site.objects.get_current().domain,
        reverse('csf.formulaire.views.preview',
                kwargs={'id': obj.etablissement_eligible.id,},
                ),
        obj.auf_auth_token.value,
        )
    if just_link:
        return link
    return mark_safe('<a href="%(link)s">%(link)s</a>' % {'link': link})
show_link.short_description = _(u'Lien')
show_link.allow_tags = True


class EtablissementEligible(models.Model):
    user = models.OneToOneField(
        User,
        related_name='etablissement_eligible',
        verbose_name="Utilisateur",
        )
    etablissement = models.OneToOneField(
        ref.Etablissement,
        related_name='etablissement_eligible',
        verbose_name="Établissement",)
    participant = models.NullBooleanField(
        default=None,
        verbose_name="Participe au programme CSF",
        )
    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
    
    @property
    def edit_link(self):
        return show_edit_link(self.user, True)

    @property
    def link(self):
        return show_link(self.user, True)

    @property
    def has_published_info(self):
        return self.offres_formation.filter(offert=True).count()
        
    def __unicode__(self):
        return self.etablissement.nom


class BaseEtablissementImages(models.Model):
    logo = models.ImageField(
        upload_to='logos',
        blank=True,
        null=True,
        )
    photo = models.ImageField(
        upload_to='etab_photos',
        blank=True,
        null=True,
        )

    class Meta:
        abstract = True


class EtablissementImages(BaseEtablissementImages):
    etablissement = models.OneToOneField(
        EtablissementEligible,
        related_name='images',
        verbose_name='Établissement',
        )


class DraftEtablissementImages(BaseEtablissementImages):
    etablissement = models.OneToOneField(
        EtablissementEligible,
        related_name='draft_images',
        verbose_name='Établissement',
        )


class BaseContactInfo(models.Model):
    prenom = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        )
    nom = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        )
    courriel = models.EmailField(
        blank=True,
        null=True,
        )
    telephone = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        )
    page_personnelle = models.URLField(
        blank=True,
        null=True,
        )

    class Meta:
        abstract = True
    

class ContactInfo(BaseContactInfo):
    etablissement = models.OneToOneField(
        EtablissementEligible,
        related_name='contact_info',
        verbose_name='Établissement',
        )


class DraftContactInfo(BaseContactInfo):
    etablissement = models.OneToOneField(
        EtablissementEligible,
        related_name='draft_contact_info',
        verbose_name='Établissement',
        )

"""
Modèles abstraits.
"""

class BaseURLEtablissement(models.Model):
    url = models.URLField(
        blank=True,
        null=True,
        )
    type = models.ForeignKey(TypeUrls)

    class Meta:
        abstract = True
        unique_together = (
            ('etablissement', 'type'),
            )

    @classmethod
    def create_missing(cls, etablissement):
        qs = cls.objects.filter(etablissement=etablissement)

        missing = TypeUrls.objects.exclude(
            id__in=qs.values_list(
                'type__id', flat=True)
            )
        
        new_urls = [
            cls(
                type=x,
                etablissement=etablissement,
                )
            for x in missing
            ]
        cls.objects.bulk_create(new_urls)
        


class BaseOffreFormation(models.Model):
    offert = models.BooleanField(default=False)

    class Meta:
        ordering=('discipline__ordering',)
        abstract = True

    @classmethod
    def create_missing(cls, etablissement):
        qs = cls.objects.filter(etablissement=etablissement)

        rows = set(itertools.product(
                Discipline.objects.all().values_list('id', flat=True),
                Niveau.objects.all().values_list('id', flat=True),
                ))
        current_products = set(
            qs.values_list('discipline', 'niveau'))

        missing = rows.difference(current_products)
        
        new_offres = [
            cls(
                discipline_id=x[0],
                niveau_id=x[1],
                etablissement_id=etablissement.id,
                )
            for x in missing
            ]
        cls.objects.bulk_create(new_offres)

"""
Classes pour entrées en préparation
"""

class DraftURLEtablissement(BaseURLEtablissement):
    etablissement = models.ForeignKey(
        EtablissementEligible,
        related_name='draft_urls')


class DraftOffreFormation(BaseOffreFormation):

    etablissement = models.ForeignKey(
        EtablissementEligible,
        related_name='draft_offres_formation')

    discipline = models.ForeignKey(
        Discipline,
        related_name='draft_offres_formation')
    
    niveau = models.ForeignKey(
        Niveau,
        related_name='draft_offres_formation')
    


"""
Classes pour entrées publiées
"""

class URLEtablissement(BaseURLEtablissement):
    etablissement = models.ForeignKey(
        EtablissementEligible,
        related_name='urls')


class OffreFormation(BaseOffreFormation):

    etablissement = models.ForeignKey(
        EtablissementEligible,
        related_name='offres_formation')

    discipline = models.ForeignKey(
        Discipline,
        related_name='offres_formation')
    
    niveau = models.ForeignKey(
        Niveau,
        related_name='offres_formation')
    
    def __unicode__(self):
        return self.etablissement.__unicode__()
