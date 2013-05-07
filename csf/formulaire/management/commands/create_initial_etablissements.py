import re
import unicodedata
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from auf.django.references import models as ref
from auf.django.auth_token.models import Token
from csf.formulaire.models import EtablissementEligible


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
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    # ref.Etablissement.filter(pays__in=('BE', 'CA', 'FR'), actif=True,
    #                          membre=True, qualite='ESR')


    def handle(self, *args, **options):
        
        eligibles = []
        for etab in ref.Etablissement.objects.filter(
                pays__in=('BE', 'CA', 'FR'), actif=True,
                membre=True, qualite='ESR'):

            etab_qs = EtablissementEligible.objects.filter(
                etablissement=etab,
                )

            if etab_qs.count() == 0:
                u, created = User.objects.get_or_create(
                    username='%s_%s' % (
                        slugify(etab.nom),
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

                e, _ = EtablissementEligible.objects.get_or_create(
                    user=u,
                    etablissement=etab,
                    participant=None,
                    )
