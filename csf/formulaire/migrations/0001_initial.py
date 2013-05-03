# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Discipline'
        db.create_table('formulaire_discipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('formulaire', ['Discipline'])

        # Adding model 'Niveau'
        db.create_table('formulaire_niveau', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('formulaire', ['Niveau'])

        # Adding model 'TypeUrls'
        db.create_table('formulaire_typeurls', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('formulaire', ['TypeUrls'])

        # Adding model 'EtablissementEligible'
        db.create_table('formulaire_etablissementeligible', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etablissement', self.gf('django.db.models.fields.related.OneToOneField')(related_name='etablissements_eligibles', unique=True, to=orm['references.Etablissement'])),
        ))
        db.send_create_signal('formulaire', ['EtablissementEligible'])

        # Adding model 'DraftEtablissementParticipant'
        db.create_table('formulaire_draftetablissementparticipant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='draft_etablissement_participant', unique=True, to=orm['auth.User'])),
            ('etablissement', self.gf('django.db.models.fields.related.OneToOneField')(related_name='draft_etablissement_participant', unique=True, to=orm['references.Etablissement'])),
        ))
        db.send_create_signal('formulaire', ['DraftEtablissementParticipant'])

        # Adding model 'DraftURLEtablissement'
        db.create_table('formulaire_drafturletablissement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formulaire.TypeUrls'])),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='urls', to=orm['formulaire.DraftEtablissementParticipant'])),
        ))
        db.send_create_signal('formulaire', ['DraftURLEtablissement'])

        # Adding unique constraint on 'DraftURLEtablissement', fields ['etablissement', 'type']
        db.create_unique('formulaire_drafturletablissement', ['etablissement_id', 'type_id'])

        # Adding model 'DraftOffreFormation'
        db.create_table('formulaire_draftoffreformation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offres_formation', to=orm['formulaire.DraftEtablissementParticipant'])),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(related_name='draft_offres_formation', to=orm['formulaire.Discipline'])),
            ('niveau', self.gf('django.db.models.fields.related.ForeignKey')(related_name='draft_offres_formation', to=orm['formulaire.Niveau'])),
        ))
        db.send_create_signal('formulaire', ['DraftOffreFormation'])

        # Adding model 'EtablissementParticipant'
        db.create_table('formulaire_etablissementparticipant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='etablissement_participant', unique=True, to=orm['auth.User'])),
            ('etablissement', self.gf('django.db.models.fields.related.OneToOneField')(related_name='etablissement_participant', unique=True, to=orm['references.Etablissement'])),
        ))
        db.send_create_signal('formulaire', ['EtablissementParticipant'])

        # Adding model 'URLEtablissement'
        db.create_table('formulaire_urletablissement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formulaire.TypeUrls'])),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='urls', to=orm['formulaire.EtablissementParticipant'])),
        ))
        db.send_create_signal('formulaire', ['URLEtablissement'])

        # Adding unique constraint on 'URLEtablissement', fields ['etablissement', 'type']
        db.create_unique('formulaire_urletablissement', ['etablissement_id', 'type_id'])

        # Adding model 'OffreFormation'
        db.create_table('formulaire_offreformation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etablissement', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offres_formation', to=orm['formulaire.EtablissementParticipant'])),
            ('discipline', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offres_formation', to=orm['formulaire.Discipline'])),
            ('niveau', self.gf('django.db.models.fields.related.ForeignKey')(related_name='offres_formation', to=orm['formulaire.Niveau'])),
        ))
        db.send_create_signal('formulaire', ['OffreFormation'])


    def backwards(self, orm):
        # Removing unique constraint on 'URLEtablissement', fields ['etablissement', 'type']
        db.delete_unique('formulaire_urletablissement', ['etablissement_id', 'type_id'])

        # Removing unique constraint on 'DraftURLEtablissement', fields ['etablissement', 'type']
        db.delete_unique('formulaire_drafturletablissement', ['etablissement_id', 'type_id'])

        # Deleting model 'Discipline'
        db.delete_table('formulaire_discipline')

        # Deleting model 'Niveau'
        db.delete_table('formulaire_niveau')

        # Deleting model 'TypeUrls'
        db.delete_table('formulaire_typeurls')

        # Deleting model 'EtablissementEligible'
        db.delete_table('formulaire_etablissementeligible')

        # Deleting model 'DraftEtablissementParticipant'
        db.delete_table('formulaire_draftetablissementparticipant')

        # Deleting model 'DraftURLEtablissement'
        db.delete_table('formulaire_drafturletablissement')

        # Deleting model 'DraftOffreFormation'
        db.delete_table('formulaire_draftoffreformation')

        # Deleting model 'EtablissementParticipant'
        db.delete_table('formulaire_etablissementparticipant')

        # Deleting model 'URLEtablissement'
        db.delete_table('formulaire_urletablissement')

        # Deleting model 'OffreFormation'
        db.delete_table('formulaire_offreformation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'formulaire.discipline': {
            'Meta': {'object_name': 'Discipline'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'formulaire.draftetablissementparticipant': {
            'Meta': {'object_name': 'DraftEtablissementParticipant'},
            'etablissement': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'draft_etablissement_participant'", 'unique': 'True', 'to': "orm['references.Etablissement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'draft_etablissement_participant'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'formulaire.draftoffreformation': {
            'Meta': {'object_name': 'DraftOffreFormation'},
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'draft_offres_formation'", 'to': "orm['formulaire.Discipline']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offres_formation'", 'to': "orm['formulaire.DraftEtablissementParticipant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niveau': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'draft_offres_formation'", 'to': "orm['formulaire.Niveau']"})
        },
        'formulaire.drafturletablissement': {
            'Meta': {'unique_together': "(('etablissement', 'type'),)", 'object_name': 'DraftURLEtablissement'},
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['formulaire.DraftEtablissementParticipant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formulaire.TypeUrls']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'formulaire.etablissementeligible': {
            'Meta': {'object_name': 'EtablissementEligible'},
            'etablissement': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'etablissements_eligibles'", 'unique': 'True', 'to': "orm['references.Etablissement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'formulaire.etablissementparticipant': {
            'Meta': {'object_name': 'EtablissementParticipant'},
            'etablissement': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'etablissement_participant'", 'unique': 'True', 'to': "orm['references.Etablissement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'etablissement_participant'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'formulaire.niveau': {
            'Meta': {'object_name': 'Niveau'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'formulaire.offreformation': {
            'Meta': {'object_name': 'OffreFormation'},
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offres_formation'", 'to': "orm['formulaire.Discipline']"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offres_formation'", 'to': "orm['formulaire.EtablissementParticipant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niveau': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offres_formation'", 'to': "orm['formulaire.Niveau']"})
        },
        'formulaire.typeurls': {
            'Meta': {'object_name': 'TypeUrls'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'formulaire.urletablissement': {
            'Meta': {'unique_together': "(('etablissement', 'type'),)", 'object_name': 'URLEtablissement'},
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['formulaire.EtablissementParticipant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formulaire.TypeUrls']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'references.bureau': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Bureau', 'db_table': "u'ref_bureau'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"})
        },
        'references.etablissement': {
            'Meta': {'ordering': "['pays__nom', 'nom']", 'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cedex': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'historique': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'implantation'", 'to': "orm['references.Implantation']"}),
            'membre': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'membre_adhesion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nombre_chercheurs': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_enseignants': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_etudiants': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nombre_membres': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to_field': "'code'", 'db_column': "'pays'", 'to': "orm['references.Pays']"}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'qualite': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'db_column': "'region'", 'to': "orm['references.Region']"}),
            'responsable_courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'responsable_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'responsable_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sigle': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'references.implantation': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'to_field': "'code'", 'db_column': "'adresse_physique_pays'", 'to': "orm['references.Pays']"}),
            'adresse_physique_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adresse_postale_boite_postale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'adresse_postale_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'to_field': "'code'", 'db_column': "'adresse_postale_pays'", 'to': "orm['references.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code_meteo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'courriel_interne': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'date_extension': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_inauguration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fuseau_horaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_convention_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'zone_administrative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.ZoneAdministrative']"})
        },
        'references.pays': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Pays', 'db_table': "u'ref_pays'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Bureau']", 'to_field': "'code'", 'null': 'True', 'db_column': "'code_bureau'", 'blank': 'True'}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['references.Region']", 'db_column': "'region'"})
        },
        'references.region': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Region', 'db_table': "u'ref_region'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gere_region'", 'null': 'True', 'db_column': "'implantation_bureau'", 'to': "orm['references.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'references.zoneadministrative': {
            'Meta': {'ordering': "['nom']", 'object_name': 'ZoneAdministrative', 'db_table': "'ref_zoneadministrative'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['formulaire']