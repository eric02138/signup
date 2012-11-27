from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField
from requestapp.models import Request, Service, LabGroup
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
        fields = ('first_name', 'last_name', 'email', 'email_confirm', 'title', 'department', 'phone')

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
        if email and not email.lower().endswith('harvard.edu'):
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
            raise forms.ValidationError(msg)
            
            del password
            del confirm_password

        #check that password is complex
        min_password_length = 8
        special_char_set = set(c for c in '~!@#$%^&*()_+')
        number_char_set = set(c for c in '1234567890')

        if ((len(password) < min_password_length) or #too short
            (password == password.lower()) or #all lowercase
            (password == password.upper()) or #all uppercase
            (not any(passchar in special_char_set for passchar in password)) or #no special chars
            (not any(passchar in number_char_set for passchar in password)) #no numbers
            ): 
            msg = u'Passwords must be at least %s characters in length, contain UPPERCASE letters, lowercase letters, at least one special ch@racter and at least 1 number.' % str(min_password_length)
            self._errors["choose_password"] = self.error_class([msg])
            #raise forms.ValidationError(msg)
            
            del password
            del confirm_password

        #check if user is already in AD
        ldap = LdapConnection()
        #search by email
        email_search = ldap.search_by_email(email)
        #search by first and last name
        name_search = ldap.search_by_firstname_lastname(first_name, last_name)

        if email_search or name_search:
            msg = '{0} {1} already has an RC account.<br />  If you have forgotten your password and need it to be reset, please <a href="mailto:mattison@g.harvard.edu?subject=\'Password Reset Request for {0} {1}\'">send an email to RCHelp</a>.'.format(first_name, last_name)
            msg = mark_safe(msg)
            raise forms.ValidationError(msg)
        ldap.unbind()

        return cleaned_data

class PIInfoForm(ModelForm):
    class Meta:
        model = LabGroup
        fields = ('name', 'pi_first_name', 'pi_last_name', 'pi_email', 'pi_phone', 'pi_mailing_address',)

    def __init__(self, **kwargs):
        super(PIInfoForm, self).__init__(**kwargs)
        self.fields['name'] = forms.ModelChoiceField(queryset=LabGroup.objects.all(), label="Lab Group", required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        email = cleaned_data.get('pi_email')
        first_name = cleaned_data.get('pi_first_name')
        last_name = cleaned_data.get('pi_last_name')
        email = cleaned_data.get('pi_email')
        phone = cleaned_data.get('pi_phone')
        mailing_address = cleaned_data.get('pi_mailing_address')

        # if the user hasn't selected a lab group from the drop-down list, make sure they have provided all the other fields
        if not name:
            if not email:
                msg = u'Please provide the Faculty Sponsor\'s email address.'
                self._errors["pi_email"] = self.error_class([msg])
                raise forms.ValidationError(msg)

            #require a harvard email address, 
            #might remove later if ldap search is authoritative
            if not email.lower().endswith('harvard.edu'):
                msg = u'Email must end with "harvard.edu".'
                self._errors["pi_email"] = self.error_class([msg])
                raise forms.ValidationError(msg)
                del cleaned_data["email"]

            if not first_name:
                msg = u'Please provide the Faculty Sponsor\'s first name.'
                self._errors["pi_first_name"] = self.error_class([msg])
                raise forms.ValidationError(msg)

            if not last_name:
                msg = u'Please provide the Faculty Sponsor\'s last name.'
                self._errors["pi_last_name"] = self.error_class([msg])
                raise forms.ValidationError(msg)

            if not phone:
                msg = u'Please provide the Faculty Sponsor\'s phone number.'
                self._errors["pi_phone"] = self.error_class([msg])
                raise forms.ValidationError(msg)

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

class ServiceChoiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ('name',)
        #widget = forms.CheckboxSelectMultiple()

    def __init__(self, is_displayed_in_signup=None, **kwargs):
        super(ServiceChoiceForm, self).__init__(**kwargs)
        self.fields['name'] = forms.ModelMultipleChoiceField(queryset=Service.objects.filter(is_displayed_in_signup=True), 
                                                             widget=forms.CheckboxSelectMultiple())
        #self.fields['name'].widget = forms.CheckboxSelectMultiple(queryset=Service.objects.filter(is_displayed_in_signup=True))

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
            if last_facility_name != instrument['facility_name']:
                self.fields['facility_names[%s]' % i] = forms.CharField(widget=forms.HiddenInput(), initial=instrument['facility_name'], required=False)
            self.fields['instruments[%s]' % i] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'free_instrument': instrument['free_instrument']}), 
                                                                  required=False, 
                                                                  label=instrument['resource'])

            resource_admin_string = "%s | %s | " % (instrument['resource'], instrument['g_group'])
            for j,resource_admin in enumerate(instrument['resource_admins']):
                resource_admin_string += "%s, %s" % (resource_admin['resource_admin_fullname'], resource_admin['resource_admin_email'])
                if j < (len(instrument['resource_admins']) - 1):
                    resource_admin_string += "; "

            self.fields['resource_admins[%s]' % i] = forms.CharField(widget=forms.HiddenInput(), initial=resource_admin_string, required=False)
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

    def clean(self):
        cleaned_data = self.cleaned_data
        for k,v in cleaned_data.iteritems():
            if ('instruments' in k) and v:
                instrument_num = k.strip('instruments[')[:-1]
                #print instrument_num
                resource_admins = cleaned_data.get('resource_admins[%s]' % instrument_num)
        return cleaned_data

class StorageChoiceForm(forms.Form):
    storage_amount = forms.IntegerField(min_value=1, max_value=5000, label="How many Gigabytes of network storage do you think you will need?")
    storage_comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 4}), label="Comment")

class SoftwareChoiceForm(forms.Form):
    software_list = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), label="Please list which software packages you require")
    queue_request = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}), label="Please list any special queue requests you have")

class OtherForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 4}), label="")

