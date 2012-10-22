from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone

class RCUser(models.Model):
    rcuser = models.ForeignKey(User)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return self.rcuser.username

class Request(models.Model):
    first_name = models.CharField(default="", null=False, max_length=100)
    last_name = models.CharField(default="", null=False, max_length=100)
    email = models.EmailField(default="", null=False)
    email_confirm = models.EmailField(default="", null=False)
    phone = PhoneNumberField(default="", null=False)

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

def do_something(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']
    print 'the object is now saved.'

post_save.connect(do_something, sender=Request)
