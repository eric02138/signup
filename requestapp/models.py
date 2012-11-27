from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
import datetime, md5
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from settings import RT_URI, RT_USER, RT_PW, RT_EMAIL, PI_APPROVAL
import rt
from ldapconnection import *


class RCUser(models.Model):
    rcuser = models.ForeignKey(User)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return self.rcuser.username

class Service(models.Model):
    name = models.CharField(default="", null=False, max_length=100)
    is_displayed_in_signup = models.BooleanField(default=False)
    doc_url = models.URLField(default="", blank=True, null=True, help_text='Link to documentation for this service')
    description = models.TextField(default="", blank=True, null=True, max_length=500)

    def __unicode__(self):
        return "%s" % (self.name)

class Request(models.Model):
    #RC Internal information
    services = models.ManyToManyField(Service, null=True)

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
    email_confirm = models.EmailField(default="", null=False, verbose_name="Please confirm that your email is correct")
    phone = PhoneNumberField(default="", null=False)
    title = models.CharField(default="", null=False, max_length=100, verbose_name="Job Position or Title")
    department = models.CharField(default="", null=False, max_length=100)
    #don't store the password in the database - send it directly to AD

    pi_first_name = models.CharField(default="", null=False, max_length=100, verbose_name="Faculty Sponsor's First Name")
    pi_last_name = models.CharField(default="", null=False, max_length=100, verbose_name="Faculty Sponsor's Last Name")
    pi_email = models.EmailField(null=False, verbose_name="Faculty Sponsor's Email Address")
    pi_phone = PhoneNumberField(default="", null=False, verbose_name="Faculty Sponsor's Phone Number")
    pi_mailing_address = models.CharField(default="", null=False, max_length=250, verbose_name="Faculty Sponsor's Mailing Address")

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

class LabGroup(models.Model):
    name = models.CharField(default="", blank=True, null=True, max_length=100, verbose_name="Lab Group")
    ad_group_name = models.CharField(default="", null=True, max_length=100, help_text="corresponding group name in RC Active Directory")
    members = models.ManyToManyField(Request)
    services = models.ManyToManyField(Service, null=True)

    pi_first_name = models.CharField(default="", blank=True, null=True, max_length=100, verbose_name="Faculty Sponsor's First Name")
    pi_last_name = models.CharField(default="", blank=True, null=True, max_length=100, verbose_name="Faculty Sponsor's Last Name")
    pi_email = models.EmailField(default="", blank=True, null=True, verbose_name="Faculty Sponsor's Email Address")
    pi_phone = PhoneNumberField(default="", blank=True, null=True, verbose_name="Faculty Sponsor's Phone Number")
    pi_mailing_address = models.TextField(default="", blank=True, null=True, max_length=250, verbose_name="Faculty Sponsor's Mailing Address")

    def __unicode__(self):
        return "%s: %s %s" % (self.name, self.pi_first_name, self.pi_last_name)

def post_save_handler(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']

    if (obj.rt_ticket_number > 0) and (obj.ignore_me == False):
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
            body += "https://rthelp.rc.fas.harvard.edu/Ticket/Display.html?id=%s\n" % (obj.rt_ticket_number) #change this later
            body += "To approve or reject this request, click here:\n"
            body += "http://%s/admin/requestapp/request/%s/\n" % ('127.0.0.1:8000', obj.pk) # change url
            send_mail(subject, body, frm, to, fail_silently=False)
        #rc rejection
        if ((obj.rc_approval == False) and
            (obj.rc_rejection == True)):

            #send rejection notice to requestor
            frm = RT_EMAIL
            to = [obj.email]
            subject = "Request for %s %s has been rejected by RC" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s %s has requested an RC account.  This request has been rejected.\n" % (obj.first_name, obj.last_name)
            body += "For more details, please contact %s\n" % RT_HELP
            send_mail(subject, body, frm, to, fail_silently=False)

            ticket_text = ""
            ticket_text += "RC rejected this request."
            tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
            tracker.login()
            tracker.edit_ticket(obj.rt_ticket_number, Action='comment', Text=ticket_text)
            tracker.logout()

        #rc approval
        if ((obj.rc_approval == True) and
            (obj.rc_rejection == False) and
            (obj.pi_approval == False) and
            (obj.pi_rejection == False)):
            #print request
            #send email to PI
            approve_link = "http://%s/request/pi-approval/%s/%s/" % ("127.0.0.1:8000", #change this
                                                                     obj.id_md5,
                                                                     md5.new(PI_APPROVAL['approved'] + str(obj.pk)).hexdigest()
                                                                     )
            reject_link = "http://%s/request/pi-approval/%s/%s/" % ("127.0.0.1:8000", #change this
                                                                    obj.id_md5,
                                                                    md5.new(PI_APPROVAL['rejected'] + str(obj.pk)).hexdigest()
                                                                    )
            frm = RT_EMAIL
            to = [obj.pi_email]
            subject = "New RC Account Request for %s %s Requires Your Approval" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s,\n" % obj.pi_first_name
            body += "\n"
            body += "%s %s (%s) has requested an RC account.  Please use the links below to verify that you approve this user's account.\n" % (obj.first_name, obj.last_name, obj.email)
            body += "\n"
            body += "I approve this account:\n"
            body += "%s\n" % approve_link
            body += "\n"
            body += "I reject this request:\n"
            body += "%s\n" % reject_link
            body += "\n"
            body += "If you have questions about this request, please contact %s or %s for more information.\n" % (obj.email, RT_EMAIL)
            send_mail(subject, body, frm, to, fail_silently=False)

            ticket_text = ""
            ticket_text += "RC approved this request."
            tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
            tracker.login()
            tracker.edit_ticket(obj.rt_ticket_number, Action='comment', Text=ticket_text)
            tracker.logout()

        #pi approval
        if ((obj.rc_approval == True) and
            (obj.rc_rejection == False) and
            (obj.pi_approval == True) and
            (obj.pi_rejection == False)):
            #Need code here to enable AD account, add account to correct lab group
            cn = str("%s %s" % (obj.first_name, obj.last_name))
            ldap_conn = LdapConnection()
            ldap_conn.enable_new_user(cn)
            new_ou = 'other_ou'
            ldap_conn.move_user(cn, new_ou)
            ldap_conn.unbind()

            #Notify Requestor
            frm = RT_EMAIL
            to = [obj.email]
            subject = "%s %s your account has been approved." % (obj.first_name, obj.last_name)
            body = ""
            body += "%s, your RC account request has been approved.\n" % (obj.first_name)
            body += "\n"
            body += "If you have questions about this request, please contact %s for more information.\n" % (RT_EMAIL)
            body += "Thank you.\n"
            send_mail(subject, body, frm, to, fail_silently=False)


            instrument_requests = obj.instrumentrequest_set.all() #reverse lookup, clever, eh?
            for instrument_request in instrument_requests:
                resource_name = instrument_request.resource_name
                resource_group = instrument_request.resource_group
                resource_administrators = instrument_request.resource_administrators.split("; ")
                #send email to resource admins
                spinal_g_group_link = "https://webapps.sciences.fas.harvard.edu/spinal/mg/members/%s/" % (resource_group)

                frm = RT_EMAIL
                to = [RT_EMAIL]
                bcc_emails = [admin.split(", ")[1] for admin in resource_administrators]
                bcc = bcc_emails
                subject = "%s %s has requested access to %s" % (obj.first_name, obj.last_name, resource_name)
                body = ""
                body += "Hello,\n"
                body += "\n"
                body += "%s %s (%s) has requested access to %s.  Please log in to SPINAL to add this user to the group %s:\n" % (
                    obj.first_name, 
                    obj.last_name, 
                    obj.email, 
                    resource_name,
                    resource_group)
                body += "%s\n" % spinal_g_group_link
                body += "\n"
                body += "If you have questions about this request, please contact %s or %s for more information.\n" % (obj.email, RT_EMAIL)
                email = EmailMessage(subject, body, frm, to, bcc)
                email.send(fail_silently=False)

            #if there's a lab admin set and they have a legit email, send email.  Otherwise, punt to RT.
            if obj.labadministrator_set.all():
                lab_administrator = obj.labadministrator_set.all()[0]
                lab_administrator_email = lab_administrator.lab_administrator_email
                lab_administrator_firstname, lab_administrator_lastname = lab_administrator.lab_administrator_name.split(" ", 1)
                lab_administrator_extra_info = lab_administrator.extra_info
                if lab_administrator_email:
                    #Need tastypie code here to create Expense Code Requests in SPINAL for each instrument requested.
                    #lookup by name?
                    
                    spinal_link = "https://webapps.sciences.fas.harvard.edu/spinal/"
                    frm = RT_EMAIL
                    to = [lab_administrator_email]
                    subject = "SPINAL Instrument Request for %s %s Requires Expense Code Assignment" % (obj.first_name, obj.last_name)
                    body = ""
                    body += "%s,\n" % lab_administrator_firstname
                    body += "\n"
                    body += "%s %s (%s) has requested the use of instrument(s) which require Harvard Expense Codes to reserve.  Please log in to SPINAL to assign the appropriate expense codes for this user.\n" % (obj.first_name, obj.last_name, obj.email)
                    body += "%s\n" % spinal_link
                    body += "\n"
                    body += "If you have questions about this request, please contact %s or %s for more information.\n" % (obj.email, RT_EMAIL)
                    body += "Thank you.\n"
                    send_mail(subject, body, frm, to, fail_silently=False)

                else: 
                    #send email to RT
                    frm = obj.email
                    to = RT_EMAIL
                    subject = "SPINAL Instrument Request for %s %s Requires Expense Code Assignment" % (obj.first_name, obj.last_name)
                    body = ""
                    body += "Hi,\n" % lab_administrator_firstname
                    body += "\n"
                    body += "%s %s (%s) has requested the use of instrument(s) which require Harvard Expense Codes to reserve.\n" % (obj.first_name, obj.last_name, obj.email)
                    body += "However, %s could not find his/her lab administrator in the drop-down list provided.  Perhaps the following information will help:\n" % obj.first_name
                    body += "%s\n" % lab_administrator_extra_info
                    body += "Thank you.\n"
                    send_mail(subject, body, frm, to, fail_silently=False)

        if ((obj.pi_approval == False) and
            (obj.pi_rejection == True)):

            #send rejection notice to requestor
            frm = RT_EMAIL
            to = [obj.email]
            subject = "Request for %s %s has been rejected by Faculty" % (obj.first_name, obj.last_name)
            body = ""
            body += "%s,\n" % obj.first_name
            body += "\n"
            body += "Sorry, your request for an RC account was rejected by %s %s.\n" % (obj.pi_first_name, obj.last_name)
            body += "\n"
            body += "For more details, please contact %s\n" % obj.pi_email
            send_mail(subject, body, frm, to, fail_silently=False)


post_save.connect(post_save_handler, sender=Request)
