from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField

class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = USPhoneNumberField()

class PIInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

class ServiceChoiceForm(forms.Form):
    needs_spinal = forms.BooleanField(required=False)
    needs_storage = forms.BooleanField(required=False)
    needs_other = forms.BooleanField(required=False)

class SpinalResourceListForm(forms.Form):
    instrument1 = forms.BooleanField(required=False)
    instrument2 = forms.BooleanField(required=False)
    instrument3 = forms.BooleanField(required=False)

class StorageChoiceForm(forms.Form):
    storage_amount = forms.IntegerField(min_value=1, max_value=10)

class OtherForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
