from django.core.management.base import BaseCommand
from auf.django.references.models import Employe
from django.contrib.auth.models import User
import random
import string


class Command(BaseCommand):
    args = ''
    help = "import_users"
    def handle(self, *args, **options):
        for e in Employe.objects.filter(courriel__isnull=False).exclude(courriel=''):
            if User.objects.filter(email=e.courriel).count() > 0:
                continue
            u = User.objects.create(
                first_name=e.prenom,
                last_name=e.nom,
                is_staff=False,
                is_active=True,
                username=(e.courriel.split('@')[0]),
                email=e.courriel,
                )
            u.set_password(''.join([string.letters[
                            random.randint(0,25)]
                                    ])
                           )
