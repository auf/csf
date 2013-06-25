# -*- encoding: utf-8 -*-

import sys
from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from csf.formulaire.models import (
    EtablissementEligible,
    Niveau,
    Discipline,
    OffreFormation,
    DraftOffreFormation,
    )


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'
    

    def get_formations_in_chunks(self, type_formation, etab):
        of_qs = [x for x in type_formation.objects.filter(
                etablissement=etab).order_by('-discipline__id', 'id')]
        n_count = Niveau.objects.count()
        return [x for x in chunks(of_qs, n_count)]


    def chunks_to_boolean_table(self, chunks):
        return [
            [x.offert for x in line] for line in chunks]
        return [x for x in chunks(of_qs, Niveau.objects.count())]
            

    def get_proper_formation_table_as_chunks(self, type_formation, etab):
        of_qs = [x for x in type_formation.objects.filter(
                etablissement=etab).order_by('-discipline__id', 'niveau__ordering')]
        n_count = Niveau.objects.count()
        return [x for x in chunks(of_qs, n_count)]


    def check_integrity(self):
        for etab in EtablissementEligible.objects.filter(
            draft_offres_formation__isnull=False):

            dof_chunks = self.get_formations_in_chunks(
                DraftOffreFormation, etab)
            d_count = Discipline.objects.all().count()
            assert(len(dof_chunks) == d_count)

            of_chunks = self.get_formations_in_chunks(
                OffreFormation, etab)
            d_count = Discipline.objects.all().count()
            assert(len(of_chunks) == d_count)


    def apply_bools_to_offers(self, bool_table, proper_table):
        fixed_offers = []
        for bools, offers in zip(bool_table, proper_table):
            for the_bool, offer in zip(bools, offers):
                if offer.offert != the_bool:
                    offer.offert = the_bool
                    fixed_offers.append(offer)
        return fixed_offers
            

    def fix_it(self):
        if (raw_input(
            'DANGER! Faites un backup de la DB avant de '
            'procéder. Inscriverz "PROCEDER" pour continuter.')
            != 'PROCEDER'):
            sys.exit()
            
        for etab in EtablissementEligible.objects.filter(
            draft_offres_formation__offert=True).distinct():

            dof_chunks = self.get_formations_in_chunks(
                DraftOffreFormation, etab)
            bool_table = self.chunks_to_boolean_table(dof_chunks)
            proper_table = self.get_proper_formation_table_as_chunks(DraftOffreFormation, etab)
            # print etab
            to_save = self.apply_bools_to_offers(bool_table, proper_table)
            [x.save() for x in to_save]
            print 'Saved these drafts:'
            pprint(to_save)

        for etab in EtablissementEligible.objects.filter(
            draft_offres_formation__offert=True).distinct():

            dof_chunks = self.get_formations_in_chunks(
                OffreFormation, etab)
            bool_table = self.chunks_to_boolean_table(dof_chunks)
            proper_table = self.get_proper_formation_table_as_chunks(OffreFormation, etab)
            # print etab
            to_save = self.apply_bools_to_offers(bool_table, proper_table)
            [x.save() for x in to_save]
            print 'Saved these offres:'
            pprint(to_save)
            

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError('1 argument max')
        elif not hasattr(self, args[0]):
            raise CommandError('Command not found.')
        else:
            return getattr(self, args[0])()
                
