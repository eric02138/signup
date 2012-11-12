from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from models import *
from forms import CaptchaForm
from signup.settings import RT_URI, RT_USER, RT_PW, PI_APPROVAL
import rt
from ldapconnection import LdapConnection

def home(request):
    return HttpResponse("You're home")

def index(request):
    return HttpResponse("You're looking at all requests.")

def is_spinal_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('servicechoices') or {}
    return cleaned_data.get('needs_spinal', True)

def is_storage_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('servicechoices') or {}
    return cleaned_data.get('needs_storage', True)

def is_software_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('servicechoices') or {}
    return cleaned_data.get('needs_software', True)

def is_other_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('servicechoices') or {}
    return cleaned_data.get('needs_other', True)

def captcha(request):
    form = CaptchaForm()
    if request.POST:
        form = CaptchaForm(request.POST)
        if form.is_valid():
            request.session['passed_captcha'] = True
            return HttpResponseRedirect('/request-wizard/')
    return render_to_response('captcha.html', { 'form': form }, context_instance=RequestContext(request))

TEMPLATES = {"userinfo": "userinfo.html",
             "piinfo": "piinfo.html",
             "servicechoices": "servicechoices.html",
             "spinalresources": "spinalresources.html",
             "storage": "storage.html",
             "softwarechoices": "software.html",
             "otherinfo": "otherinfo.html"}

class RequestWizard(SessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def render(self, form=None, **kwargs):
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        passed_captcha = self.request.session.get('passed_captcha')
        if not passed_captcha:
            #log the IP of the attempt?
            return HttpResponseRedirect('/request/')
        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
            
        #Format the data for output and filter out unnecessary instrument fields
        #This is a bit of a pain: form wizard expects a list of dicts - you can't name them.  Which sucks further down in the code...

        data_list = {}
        for form in form_list:
            form_dict = {}
            if form.prefix == 'spinalresources':
                #only add information for selected instruments
                for k,v in form.cleaned_data.iteritems():
                    if ('instruments' in k) and v:
                        #form_dict[k] = v  This doesn't really tell us much
                        instrument_num = k.strip('instruments[')[:-1]
                        form_dict['resource_admins[%s]' % instrument_num] = form.cleaned_data.get('resource_admins[%s]' % instrument_num)
                    if ('lab_administrators' in k) or ('extra_info' in k):
                        form_dict[k] = v
            else:
                for k,v in form.cleaned_data.iteritems():
                    form_dict[k] = v
            data_list.update({form.prefix: form_dict})
        
        #Save the Request
        request = Request()
        for name, form in data_list.iteritems():
            for k,v in form.iteritems():
                request.set_attr(k, v)
        request.save()

        #Save the LabAdmins and InstrumentRequests
        for name, form in data_list.iteritems():
            if name == 'spinalresources':
                for k,v in form.iteritems():
                    if 'resource_admins' in k:
                        instrument_request = InstrumentRequest()
                        resource_name, resource_group, resource_administrators = v.split(" | ")
                        instrument_request.resource_name = resource_name
                        instrument_request.resource_group = resource_group
                        instrument_request.resource_administrators = resource_administrators
                        instrument_request.request = request
                        instrument_request.save()

                    if ((k == 'lab_administrators') and v) or ((k == 'extra_info') and v):
                        lab_administrator = LabAdministrator() #request only one admin for all resources
                        if (k == 'lab_administrators') and (v != ""):
                            lab_admin_email, lab_admin_name = v.split(" - ")
                            lab_administrator.lab_administrator_name = lab_admin_name
                            lab_administrator.lab_administrator_email = lab_admin_email
                        if (k == 'extra_info' and v != ""):
                            lab_administrator.extra_info = v
                        lab_administrator.request = request
                        lab_administrator.save()

        #create RT Ticket
        subject_text = "Account Request for %s %s" % (data_list['userinfo']['first_name'], data_list['userinfo']['last_name'])
        ticket_text = ""
        ticket_text += "User Info:\n"
        ticket_text += " - First Name: %s\n" % (data_list['userinfo']['first_name'])
        ticket_text += " - Last Name: %s\n" % (data_list['userinfo']['last_name'])
        ticket_text += " - Email: %s\n" % (data_list['userinfo']['email'])
        ticket_text += " - Phone: %s\n" % (data_list['userinfo']['phone'])
        ticket_text += " Faculty Sponsor:\n"
        ticket_text += " - PI First Name: %s\n" % (data_list['piinfo']['pi_first_name'])
        ticket_text += " - PI Last Name: %s\n" % (data_list['piinfo']['pi_last_name'])
        ticket_text += " - PI Email: %s\n" % (data_list['piinfo']['pi_email'])

        if data_list['servicechoices']['needs_spinal']:
            ticket_text += " User needs instrument access.  See below.\n"

        if data_list['servicechoices']['needs_storage']:
            ticket_text += " User needs network storage.  See below.\n"

        if data_list['servicechoices']['needs_software']:
            ticket_text += " User needs Odyssey Software.  See below.\n"

        if data_list['servicechoices']['needs_other']:
            ticket_text += " User has other needs.  See below.\n"

        if 'spinalresources' in data_list:
            ticket_text += " Spinal Resources\n"
            for k,v in data_list['spinalresources'].iteritems():
                if (('lab_administrators' in k) or 
                    ('extra_info' in k)):
                    ticket_text += " - %s: %s\n" % (k,v)
                else:
                    ticket_text += " - %s\n" % (v)

        if 'softwarechoices' in data_list:
            ticket_text += " Software Choices\n"
            for k,v in data_list['softwarechoices'].iteritems():
                ticket_text += " - %s: %s\n" % (k, v)

        if 'storage' in data_list:
            ticket_text += " Storage\n"
            for k,v in data_list['storage'].iteritems():
                ticket_text += " - %s: %s\n" % (k, v)

        if 'otherinfo' in data_list:
            ticket_text += " Other Comments\n"
            for k,v in data_list['otherinfo'].iteritems(): 
                ticket_text += " - %s: %s\n" % (k, v)

        tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
        tracker.login()
        ticket_num = tracker.create_ticket(Queue='AccountRequest', Subject=subject_text, Text=ticket_text)
        tracker.logout()

        if ticket_num:
            request.rt_ticket_number = ticket_num
            request.save()

        #Add user to AD
        ldap_conn = LdapConnection()
        cn = str("%s %s" % (data_list['userinfo']['first_name'], data_list['userinfo']['last_name']))
        email = str(data_list['userinfo']['email'])
        phone = str(data_list['userinfo']['phone'])
        title = str(data_list['userinfo']['title'])
        department = str(data_list['userinfo']['department'])
        ldap_conn.add_user(cn, email, phone, title, department)
        pw = str(data_list['userinfo']['choose_password'])
        ldap_conn.set_password(cn, pw)
        #ldap_conn.enable_new_user(cn)
        ldap_conn.unbind()
        
        return render_to_response('formtools/wizard/done.html', {'data_list': data_list},)

def pi_approval(r, id_md5, approval_option_md5):
    data = {}
    #get the request
    try:
        request = Request.objects.get(id_md5=id_md5)
    except Request.DoesNotExist:
        data.update({ 'err_pi_approval': True, 'err_request_not_found': True})
        return render_to_response('pi_approval.html', data, context_instance=RequestContext(r))

    #check to see if the approval string is valid
    pk = request.pk
    status_options = [md5.new(option + str(pk)).hexdigest() for option in PI_APPROVAL]
    try:
        assert(approval_option_md5 in status_options)
    except AssertionError:
        data.update({ 'err_invalid_approval': True })
        return render_to_response('pi_approval.html', data, context_instance=RequestContext(r))

    status_dict = dict([(k, md5.new(v + str(pk)).hexdigest()) for (k,v) in PI_APPROVAL.items()])
    #change the ticket based on the choice

    data.update({ 'first_name': request.first_name })
    data.update({ 'last_name': request.last_name })
    ticket_num = request.rt_ticket_number

    if approval_option_md5 == status_dict['approved']:
        request.pi_approval = True
        request.pi_rejection = False
        request.save()
        data.update({ 'approval_status': 'approved' })

        ticket_text = ""
        ticket_text += "PI %s %s (%s) approved this request." % (request.pi_first_name, request.pi_last_name, request.pi_email)
        tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
        tracker.login()
        tracker.comment(ticket_num, text=ticket_text)
        tracker.logout()

    else:
        request.pi_approval = False
        request.pi_rejection = True
        request.save()
        data.update({ 'approval_status': 'rejected' })

        ticket_text = ""
        ticket_text += "PI %s %s (%s) rejected this request." % (request.pi_first_name, request.pi_last_name, request.pi_email)
        tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
        tracker.login()
        tracker.edit_ticket(ticket_num, Action='comment', Text=ticket_text)
        tracker.logout()

    return render_to_response('pi_approval.html', data, context_instance=RequestContext(r))
