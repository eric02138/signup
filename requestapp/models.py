from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
import datetime, md5
from django.utils import timezone
from django.core.mail import send_mail
from signup.settings import PI_APPROVAL

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
    id_md5 = models.CharField(max_length=200, blank=True, null=True, help_text="Auto-filled on save")

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
        if not self.id_md5:
            super(Request, self).save()      # save to have an 'id'
            self.id_md5 =  md5.new(str(self.id)).hexdigest()
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
        #new ticket        
        if ((obj.rc_approval == False) and
            (obj.rc_rejection == False) and
            (obj.pi_approval == False) and
            (obj.pi_rejection == False)):

            #send ticket to RCHelp
            frm = obj.email
            to = ["eric_mattison@harvard.edu"] #change this to RCHelp@fas.harvard.edu
            subject = "New Account Request for %s %s" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s %s has requested an RC account.\n" % (obj.first_name, obj.last_name)
            body += "To take this ticket, click here:\n"
            body += "https://rthelp.rc.fas.harvard.edu/Ticket/Display.html?id=%s\n" % (obj.rt_ticket_number)
            body += "To approve or reject this request, click here:\n"
            body += "http://127.0.0.1:8000/admin/requestapp/request/%s/\n" % (obj.pk)
            send_mail(subject, body, frm, to, fail_silently=False)
        #rc rejection
        if ((obj.rc_approval == False) and
            (obj.rc_rejection == True)):

            #send rejection notice to requestor
            frm = 'rchelp@fas.harvard.edu'
            to = [obj.email]
            subject = "Request for %s %s has been Rejected" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s %s has requested an RC account.  This request has been rejected.\n" % (obj.first_name, obj.last_name)
            body += "For more details, please contact rchelp@fas.harvard.edu\n"
            send_mail(subject, body, frm, to, fail_silently=False)
        #rc approval
        if ((obj.rc_approval == True) and
            (obj.rc_rejection == False) and
            (obj.pi_approval == False) and
            (obj.pi_rejection == False)):

            #send email to PI
            approve_link = "http://%s/request/pi-approval/%s/%s/" % ('127.0.0.1:8000', #change this
                                                                     obj.id_md5,
                                                                     md5.new(PI_APPROVAL['approved'] + str(obj.pk)).hexdigest()
                                                                     )
            reject_link = "http://%s/request/pi-approval/%s/%s/" % ('127.0.0.1:8000', #change this
                                                                    obj.id_md5,
                                                                    md5.new(PI_APPROVAL['rejected'] + str(obj.pk)).hexdigest()
                                                                    )
            frm = 'rchelp@fas.harvard.edu'
            to = [obj.pi_email]
            subject = "New RC Account Request for %s %s Requires Your Approval" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s %s (%s) has requested an RC account.  Please use the links below to verify that you approve this user's account.\n" % (obj.first_name, obj.last_name, obj.email)
            body += "I approve this account:\n"
            body += "%s\n" % approve_link
            body += "I reject this request:\n"
            body += "%s\n" % reject_link
            body += "If you have questions about this request, please contact %s or rchelp@fas.harvard.edu for more information.\n" % (obj.email)
            send_mail(subject, body, frm, to, fail_silently=False)

        if obj.pi_approval:
            print "send email to lab admin, resource admin"

post_save.connect(post_save_handler, sender=Request)
