from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.forms import ModelForm
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone

class RCUser(models.Model):
    rcuser = models.ForeignKey(User)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __unicode__(self):
        return self.rcuser.username

class Request(models.Model):
    rcuser = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        #return self.rcuser.__unicode__()
        return "%s, created: %s" % (self.rcuser.__unicode__(), self.created.strftime("%Y-%m-%d %H:%M:%S"))

    def is_old(self):
        return self.last_update <= timezone.now() - datetime.timedelta(days=3)
