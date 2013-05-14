# -*- encoding: utf-8 -*-

import itertools
from django.db import models
from django.contrib.auth.models import User
from auf.django.references import models as ref
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

    class Meta:
        ordering = ['ordering']
        verbose_name = _(u'Type d\'URL')
        verbose_name_plural = _(u'Types d\'URL')

    def __unicode__(self):
        return self.display_name


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
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
    
    def __unicode__(self):
        return self.etablissement.nom


class ContactInfo(models.Model):
    etablissement = models.OneToOneField(
        EtablissementEligible,
        related_name='contact_info',
        verbose_name='Établissement',
        )
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
        return "%s" % (self.etablissement, )
