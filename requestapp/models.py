from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone

class RCUser(models.Model):
    rcuser = models.ForeignKey(User)
    phone_number = PhoneNumberField()

    def __unicode__(self):
        return self.rcuser.username

class Request(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    email_confirm = models.EmailField()
    phone = PhoneNumberField()

    pi_first_name = models.CharField(max_length=100)
    pi_last_name = models.CharField(max_length=100)
    pi_email = models.EmailField()

    def __unicode__(self):
        return "%s %s" % (first_name, last_name)

