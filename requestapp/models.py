from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone
from django.core.mail import send_mail

class RCUser(models.Model):
    rcuser = models.ForeignKey(User)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return self.rcuser.username

class Request(models.Model):
    #RC Internal information
    rt_ticket_number = models.IntegerField(default=0)
    rc_approval = models.BooleanField(default=False)
    rc_rejection = models.BooleanField(default=False)
    pi_approval = models.BooleanField(default=False)
    pi_rejection = models.BooleanField(default=False)
    req_created = models.DateTimeField(auto_now_add=True)
    req_last_modified = models.DateTimeField(auto_now=True)

    #UserInfo
    first_name = models.CharField(default="", null=False, max_length=100)
    last_name = models.CharField(default="", null=False, max_length=100)
    email = models.EmailField(default="", null=False)
    email_confirm = models.EmailField(default="", null=False)
    phone = PhoneNumberField(default="", null=False)
    #don't store the password in the database - send it directly to AD

    pi_first_name = models.CharField(default="", null=False, max_length=100)
    pi_last_name = models.CharField(default="", null=False, max_length=100)
    pi_email = models.EmailField(null=False)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def set_attr(self, key, value):
        try:
            self.__dict__[key] = value
        except:
            print "field does not exist"
            return False
        return self
        
    def save(self, *args, **kwargs):
        super(Request, self).save(*args, **kwargs)

class InstrumentRequest(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.request, self.resource_name) 

    request = models.ForeignKey(Request)

    resource_name = models.CharField(default="", null=False, max_length=200)
    resource_group = models.CharField(default="", null=False, max_length=50)
    resource_administrators = models.CharField(default="", null=False, max_length=500)

class LabAdministrator(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.lab_administrator_name, self.lab_administrator_email) 


    request = models.ForeignKey(Request)

    lab_administrator_name = models.CharField(default="", null=False, max_length=50)
    lab_administrator_email = models.EmailField(default="", null=False)
    extra_info = models.CharField(default="", null=True, max_length=500)

def post_save_handler(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']

    if obj.rt_ticket_number > 0:
        if ((obj.rc_approval == False) and
            (obj.rc_rejection == False) and
            (obj.pi_approval == False) and
            (obj.pi_rejection == False)):
            print "sending mail to RC."
            #new ticket
            frm = "bobo@harvard.edu" #change this
            to = ["eric_mattison@harvard.edu"] #change this
            subject = "New Account Request for %s %s" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s %s has requested an RC account.\n" % (obj.first_name, obj.last_name)
            body += "https://rthelp.rc.fas.harvard.edu/Ticket/Display.html?id=%s\n" % (obj.rt_ticket_number)
            body += "http://127.0.0.1:8000/admin/requestapp/request/%s/\n" % (obj.pk)
            send_mail(subject, body, frm, to, fail_silently=False)
        if obj.rc_approval:
            print "send email to PI"
        if obj.pi_approval:
            print "send email to lab admin, resource admin"

post_save.connect(post_save_handler, sender=Request)
