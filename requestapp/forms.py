from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField

class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.USPhoneNumberField()

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
