# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Service.description'
        db.alter_column('requestapp_service', 'description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True))
        # Adding field 'LabGroup.pi_first_name'
        db.add_column('requestapp_labgroup', 'pi_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'LabGroup.pi_last_name'
        db.add_column('requestapp_labgroup', 'pi_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'LabGroup.pi_email'
        db.add_column('requestapp_labgroup', 'pi_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)

        # Adding field 'LabGroup.pi_phone'
        db.add_column('requestapp_labgroup', 'pi_phone',
                      self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'LabGroup.pi_mailing_address'
        db.add_column('requestapp_labgroup', 'pi_mailing_address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Service.description'
        db.alter_column('requestapp_service', 'description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))
        # Deleting field 'LabGroup.pi_first_name'
        db.delete_column('requestapp_labgroup', 'pi_first_name')

        # Deleting field 'LabGroup.pi_last_name'
        db.delete_column('requestapp_labgroup', 'pi_last_name')

        # Deleting field 'LabGroup.pi_email'
        db.delete_column('requestapp_labgroup', 'pi_email')

        # Deleting field 'LabGroup.pi_phone'
        db.delete_column('requestapp_labgroup', 'pi_phone')

        # Deleting field 'LabGroup.pi_mailing_address'
        db.delete_column('requestapp_labgroup', 'pi_mailing_address')


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
        'requestapp.instrumentrequest': {
            'Meta': {'object_name': 'InstrumentRequest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['requestapp.Request']"}),
            'resource_administrators': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'resource_group': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'resource_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'requestapp.labadministrator': {
            'Meta': {'object_name': 'LabAdministrator'},
            'extra_info': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_administrator_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'lab_administrator_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['requestapp.Request']"})
        },
        'requestapp.labgroup': {
            'Meta': {'object_name': 'LabGroup'},
            'ad_group_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['requestapp.Request']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'pi_first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_mailing_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'pi_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['requestapp.Service']", 'null': 'True', 'symmetrical': 'False'})
        },
        'requestapp.rcuser': {
            'Meta': {'object_name': 'RCUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rcuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'requestapp.request': {
            'Meta': {'object_name': 'Request'},
            'department': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'email_confirm': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_md5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'pi_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pi_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'pi_first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_mailing_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'pi_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'pi_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'req_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'req_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rt_ticket_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['requestapp.Service']", 'null': 'True', 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'requestapp.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'doc_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_displayed_in_signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['requestapp']