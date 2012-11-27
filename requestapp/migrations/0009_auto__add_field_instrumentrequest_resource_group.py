# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InstrumentRequest.resource_group'
        db.add_column('requestapp_instrumentrequest', 'resource_group',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InstrumentRequest.resource_group'
        db.delete_column('requestapp_instrumentrequest', 'resource_group')


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
        'requestapp.rcuser': {
            'Meta': {'object_name': 'RCUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rcuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'requestapp.request': {
            'Meta': {'object_name': 'Request'},
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'email_confirm': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'pi_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pi_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'pi_first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'pi_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'req_created': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'auto_now_add': 'True', 'blank': 'True'}),
            'req_last_modified': ('django.db.models.fields.DateTimeField', [], {'default': "''", 'auto_now': 'True', 'blank': 'True'}),
            'rt_ticket_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['requestapp']