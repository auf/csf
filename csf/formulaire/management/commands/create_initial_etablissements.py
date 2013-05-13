# -*- encoding: utf-8 -*-
import re
import unicodedata
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from auf.django.references import models as ref
from auf.django.auth_token.models import Token
from csf.formulaire.models import (
    EtablissementEligible,
    OffreFormation,
    DraftURLEtablissement,
    TypeUrls,
    )


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Taken from Django.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


class Command(BaseCommand):
    args = ''
    help = ''


    def handle(self, *args, **options):
        
        accueil_url = None
        eligibles = []
        for t_url in TypeUrls.objects.all():
            print '[%s] %s' % (
                t_url.id,
                t_url.display_name,
                )
        accueil_id = raw_input(
            'SVP entrez l\'id du type d\'url utilisé pour la '
            'page d\'accueil: ')
        acc_qs = TypeUrls.objects.filter(id=accueil_id)
        if acc_qs.count() == 1:
            accueil_url = acc_qs.get()


        for etab in ref.Etablissement.objects.filter(
                pays__in=('BE', 'CA', 'FR'), actif=True,
                membre=True, qualite='ESR'):

            etab_qs = EtablissementEligible.objects.filter(
                etablissement=etab,
                )

            etab_eli = None

            if etab_qs.count() == 0:
                u, created = User.objects.get_or_create(
                    username='%s_%s' % (
                        slugify(etab.nom)[:26],
                        etab.pk,
                        ),
                    email=etab.responsable_courriel or '',)

                if created:
                    u.set_unusable_password()
                    u.save()
                    Token.objects.create(
                        value=get_random_string(48),
                        user=u,
                        sent_by_email=False,
                        )

                etab_eli, _ = (
                    EtablissementEligible.objects.get_or_create(
                        user=u,
                        etablissement=etab,
                        participant=None,
                    ))

            if etab_eli and accueil_url and etab.url:
                draft_url_accueil, created = (
                    DraftURLEtablissement.objects.get_or_create(
                        etablissement=etab_eli,
                        type=accueil_url,
                        ))
                if created :
                    draft_url_accueil.url = etab.url
                    draft_url_accueil.save()
