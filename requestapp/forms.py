from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField
from requestapp.models import Request
from django.contrib.localflavor.us.forms import USPhoneNumberField
from ldapconnection import LdapConnection
import json, urllib

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()

class UserInfoForm(ModelForm):
    choose_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = Request
        fields = ('first_name', 'last_name', 'email', 'email_confirm', 'phone')

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password = cleaned_data.get('choose_password')
        confirm_password = cleaned_data.get('confirm_password')

        #make sure email and email confirm match
        if email != email_confirm:
            msg = u'Confirmation Email does not match Email.  Please try again.'
            self._errors["email"] = self.error_class("")
            self._errors["email_confirm"] = self.error_class([msg])
            raise forms.ValidationError(msg)

            del cleaned_data["email"]
            del cleaned_data["email_confirm"]

        #require a harvard email address
        if not email.lower().endswith('harvard.edu'):
            msg = u'Email must end with "harvard.edu".'
            self._errors["email"] = self.error_class([msg])
            self._errors["email_confirm"] = self.error_class("")
            raise forms.ValidationError(msg)
            
            del cleaned_data["email"]
            del cleaned_data["email_confirm"]            

        #check password matches
        if password != confirm_password:
            msg = u'Your passwords don\'t match.  Please retype your password.'
            self._errors["choose_password"] = self.error_class([msg])
            #raise forms.ValidationError(msg)
            
            del password
            del confirm_password

        #check if password meets AD's requirements
        ldap = LdapConnection()
        #result = ldap.check_password_complexity
        ldap.unbind()

        #check if user is already in AD
        ldap = LdapConnection()
        #search by email
        email_search = ldap.search_by_email(email)
        #search by first and last name
        name_search = ldap.search_by_firstname_lastname(first_name, last_name)
        ldap.unbind()

        if email_search or name_search:
            msg = '{0} {1} already has an RC account.<br />  If you have forgotten your password and need it to be reset, please <a href="mailto:mattison@g.harvard.edu?subject=\'Password Reset Request for {0} {1}\'">send an email to RCHelp</a>.'.format(first_name, last_name)
            msg = mark_safe(msg)
            raise forms.ValidationError(msg)

        return cleaned_data

class PIInfoForm(ModelForm):
    class Meta:
        model = Request
        fields = ('pi_first_name', 'pi_last_name', 'pi_email')

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('pi_email')
        first_name = cleaned_data.get('pi_first_name')
        last_name = cleaned_data.get('pi_last_name')

        #require a harvard email address
        if not email.lower().endswith('harvard.edu'):
            msg = u'Email must end with "harvard.edu".'
            self._errors["pi_email"] = self.error_class([msg])
            raise forms.ValidationError(msg)
            
            del cleaned_data["email"]

        """ Removed, but might be useful in the future
        #check if PI is not in AD
        ad_result = []
        ldap = LdapConnection()
        #search by email
        email_search = ldap.search_by_email(email)
        #search by first and last name
        name_search = ldap.search_by_firstname_lastname(first_name, last_name)
        ldap.unbind()

        if not (email_search or name_search):
            msg = '{0} {1} is not a valid Harvard Principal Investigator.'.format(first_name, last_name)
            msg = mark_safe(msg)
            raise forms.ValidationError(msg)
        """
        return cleaned_data

class ServiceChoiceForm(forms.Form):
    needs_spinal = forms.BooleanField(required=False)
    needs_storage = forms.BooleanField(required=False)
    needs_other = forms.BooleanField(required=False)

class SpinalResourceListForm(forms.Form):
    #get the list of instruments and lab admins from 
    #https://webapps.sciences.fas.harvard.edu/spinal/api/v1/resources/?format=json
    #https://webapps.sciences.fas.harvard.edu/spinal/api/v1/labadmins/?format=json
    def __init__(self, *args, **kwargs):
        super(SpinalResourceListForm, self).__init__(*args, **kwargs)

        #Get instruments via JSON
        url = 'https://webapps.sciences.fas.harvard.edu/spinal/api/v1/resources/?format=json'
        f = urllib.urlopen(url)
        contents = f.read()
        json_string = json.loads(contents)
        instrument_list = json_string['objects']

        last_facility_name = ''
        for i, instrument in enumerate(instrument_list):
            print instrument['resource'], instrument['facility_name']
            if last_facility_name != instrument['facility_name']:
                self.fields['facility_name_%s' % i] = forms.CharField(widget=forms.HiddenInput(), initial=instrument['facility_name'], required=False)
            self.fields['instrument_%s' % i] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'free_instrument': instrument['free_instrument']}), 
                                                                  required=False, 
                                                                  label=instrument['resource'])

            resource_admin_string = "%s | %s | " % (instrument['resource'], instrument['g_group'])
            for j,resource_admin in enumerate(instrument['resource_admins']):
                resource_admin_string += "%s, %s" % (resource_admin['resource_admin_fullname'], resource_admin['resource_admin_email'])
                print "j: ", j
                print "inst len: ", len(instrument['resource_admins'])
                if j < (len(instrument['resource_admins']) - 1):
                    resource_admin_string += "; "

            self.fields['resource_admins_%s' % i] = forms.CharField(widget=forms.HiddenInput(), initial=resource_admin_string, required=False)
            last_facility_name = instrument['facility_name']
            
        #Get Labs (and admins) via JSON
        url = 'https://webapps.sciences.fas.harvard.edu/spinal/api/v1/lab_groups/?format=json'
        f = urllib.urlopen(url)
        contents = f.read()
        json_string = json.loads(contents)
        lab_list = json_string['objects']

        lab_admin_tuple = []
        lab_admin_tuple.append(('','-------------'))
        for lab in lab_list:
            for lab_admin in lab['lab_admins']:
                choice_display = "%s - %s" % (lab['name'], lab_admin['lab_admin_fullname'])
                choice_value = "%s - %s" % (lab_admin['lab_admin_email'], lab_admin['lab_admin_fullname'])
                lab_admin_tuple.append((choice_value, choice_display))
        self.fields['lab_administrators'] = forms.ChoiceField(choices=lab_admin_tuple, required=False)

        self.fields['extra_info'] = forms.CharField(widget=forms.Textarea, required=False)

class StorageChoiceForm(forms.Form):
    storage_amount = forms.IntegerField(min_value=1, max_value=10)

class OtherForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

