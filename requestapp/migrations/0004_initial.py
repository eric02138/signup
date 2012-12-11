# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RCUser'
        db.create_table('requestapp_rcuser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(default='', max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('department', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('requestapp', ['RCUser'])

        # Adding model 'PIUser'
        db.create_table('requestapp_piuser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(default='', max_length=20)),
            ('mailing_address', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
        ))
        db.send_create_signal('requestapp', ['PIUser'])

        # Adding model 'Service'
        db.create_table('requestapp_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('is_displayed_in_signup', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('doc_url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('requestapp', ['Service'])

        # Adding model 'Request'
        db.create_table('requestapp_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rt_ticket_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rc_approval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rc_rejection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pi_approval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pi_rejection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('req_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('req_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('id_md5', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('rcuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requestapp.RCUser'])),
            ('pi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requestapp.PIUser'])),
        ))
        db.send_create_signal('requestapp', ['Request'])

        # Adding M2M table for field services on 'Request'
        db.create_table('requestapp_request_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm['requestapp.request'], null=False)),
            ('service', models.ForeignKey(orm['requestapp.service'], null=False))
        ))
        db.create_unique('requestapp_request_services', ['request_id', 'service_id'])

        # Adding model 'InstrumentRequest'
        db.create_table('requestapp_instrumentrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requestapp.Request'])),
            ('resource_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('resource_group', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('resource_administrators', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
        ))
        db.send_create_signal('requestapp', ['InstrumentRequest'])

        # Adding model 'LabAdministrator'
        db.create_table('requestapp_labadministrator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requestapp.Request'])),
            ('lab_administrator_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('lab_administrator_email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(default='', max_length=500, null=True)),
        ))
        db.send_create_signal('requestapp', ['LabAdministrator'])

        # Adding model 'LabGroup'
        db.create_table('requestapp_labgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('ad_group_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True)),
            ('pi', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['requestapp.PIUser'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('requestapp', ['LabGroup'])

        # Adding M2M table for field members on 'LabGroup'
        db.create_table('requestapp_labgroup_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('labgroup', models.ForeignKey(orm['requestapp.labgroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('requestapp_labgroup_members', ['labgroup_id', 'user_id'])

        # Adding M2M table for field services on 'LabGroup'
        db.create_table('requestapp_labgroup_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('labgroup', models.ForeignKey(orm['requestapp.labgroup'], null=False)),
            ('service', models.ForeignKey(orm['requestapp.service'], null=False))
        ))
        db.create_unique('requestapp_labgroup_services', ['labgroup_id', 'service_id'])


    def backwards(self, orm):
        # Deleting model 'RCUser'
        db.delete_table('requestapp_rcuser')

        # Deleting model 'PIUser'
        db.delete_table('requestapp_piuser')

        # Deleting model 'Service'
        db.delete_table('requestapp_service')

        # Deleting model 'Request'
        db.delete_table('requestapp_request')

        # Removing M2M table for field services on 'Request'
        db.delete_table('requestapp_request_services')

        # Deleting model 'InstrumentRequest'
        db.delete_table('requestapp_instrumentrequest')

        # Deleting model 'LabAdministrator'
        db.delete_table('requestapp_labadministrator')

        # Deleting model 'LabGroup'
        db.delete_table('requestapp_labgroup')

        # Removing M2M table for field members on 'LabGroup'
        db.delete_table('requestapp_labgroup_members')

        # Removing M2M table for field services on 'LabGroup'
        db.delete_table('requestapp_labgroup_services')


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
            'ad_group_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pi': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['requestapp.PIUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['requestapp.Service']", 'null': 'True', 'symmetrical': 'False'})
        },
        'requestapp.piuser': {
            'Meta': {'object_name': 'PIUser', '_ormbases': ['auth.User']},
            'mailing_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'requestapp.rcuser': {
            'Meta': {'object_name': 'RCUser', '_ormbases': ['auth.User']},
            'department': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'default': "''", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'requestapp.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_md5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['requestapp.PIUser']"}),
            'pi_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pi_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rc_rejection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rcuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['requestapp.RCUser']"}),
            'req_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'req_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rt_ticket_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['requestapp.Service']", 'null': 'True', 'symmetrical': 'False'})
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