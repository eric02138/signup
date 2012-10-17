from django import forms
from django.forms import ModelForm
from requestapp.models import Request
from django.contrib.localflavor.us.forms import USPhoneNumberField

class UserInfoForm(ModelForm):
    class Meta:
        model = Request
        fields = ('first_name', 'last_name', 'email', 'email_confirm', 'phone')

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')

        if email != email_confirm:
            msg = u'Confirmation Email does not match Email.  Please try again.'
            self._errors["email"] = self.error_class("")
            self._errors["email_confirm"] = self.error_class([msg])
            raise forms.ValidationError(msg)

            del cleaned_data["email"]
            del cleaned_data["email_confirm"]
            
        return cleaned_data

class PIInfoForm(ModelForm):
    class Meta:
        model = Request
        fields = ('pi_first_name', 'pi_last_name', 'pi_email')

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
