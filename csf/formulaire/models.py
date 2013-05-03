# -*- encoding: utf-8 -*-

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
    
    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
    
    def __unicode__(self):
        return self.etablissement.nom


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


class BaseOffreFormation(models.Model):
    offert = models.BooleanField(default=False)

    class Meta:
        abstract = True


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
    
