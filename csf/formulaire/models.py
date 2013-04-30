# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from auf.django.references import models as ref


class Discipline(models.Model):
    display_name = models.CharField(
        max_length=255,
        )
    ordering = models.IntegerField(
        default=0,
        )

    def __unicode__(self):
        return self.display_name


class Niveau(models.Model):
    ordering = models.IntegerField(
        default=0,
        )
    display_name = models.CharField(
        max_length=255,
        )

    def __unicode__(self):
        return self.display_name


class TypeUrls(models.Model):
    required = models.BooleanField(
        default=False
        )
    ordering = models.IntegerField(
        default=0,
        )
    display_name = models.CharField(
        max_length=255,
        )

    def __unicode__(self):
        return self.display_name


class EtablissementEligible(models.Model):
    user = models.OneToOneField(User)
    etablissement = models.OneToOneField(
        ref.Etablissement,
        related_name='etablissements_eligibles')
    participant = models.BooleanField(
        default=False,
        )
    
    def __unicode__(self):
        return self.etablissement.nom


"""
Modèles abstraits.
"""

class BaseURLEtablissement(models.Model):
    url = models.URLField()
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
    
