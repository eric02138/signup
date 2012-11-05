from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from models import *
from forms import CaptchaForm
from signup.settings import RT_URI, RT_USER, RT_PW
import rt

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
        data_list = []
        for form in form_list:
            form_dict = {}
            form_dict['prefix'] = form.prefix
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
            data_list.append(form_dict)
        
        #Save the Request
        request = Request()
        for form in data_list:
            for k,v in form.iteritems():
                request.set_attr(k, v)
        request.save()

        #Save the LabAdmins and InstrumentRequests
        for form in data_list:
            if form['prefix'] == 'spinalresources':
                lab_administrator = LabAdministrator() #request only one admin for all resources
                for k,v in form.iteritems():
                    if 'resource_admins' in k:
                        instrument_request = InstrumentRequest()
                        resource_name, resource_group, resource_administrators = v.split(" | ")
                        instrument_request.resource_name = resource_name
                        instrument_request.resource_group = resource_group
                        instrument_request.resource_administrators = resource_administrators
                        instrument_request.request = request
                        instrument_request.save()

                    if (k == 'lab_administrators') or (k == 'extra_info'):
                        if (k == 'lab_administrators') and (v != ""):
                            lab_admin_email, lab_admin_name = v.split(" - ")
                            lab_administrator.lab_administrator_name = lab_admin_name
                            lab_administrator.lab_administrator_email = lab_admin_email
                        if (k == 'extra_info' and v != ""):
                            lab_administrator.extra_info = v
                        lab_administrator.request = request
                        lab_administrator.save()

        #create RT Ticket
        subject_text = "Account Request for %s %s" % (data_list[0]['first_name'], data_list[0]['last_name'])
        ticket_text = ""
        ticket_text += "User Info:\n"
        ticket_text += " - First Name: %s\n" % (data_list[0]['first_name'])
        ticket_text += " - Last Name: %s\n" % (data_list[0]['last_name'])
        ticket_text += " - Email: %s\n" % (data_list[0]['email'])
        ticket_text += " - Phone: %s\n" % (data_list[0]['phone'])
        ticket_text += " Faculty Sponsor:\n"
        ticket_text += " - PI First Name: %s\n" % (data_list[1]['pi_first_name'])
        ticket_text += " - PI Last Name: %s\n" % (data_list[1]['pi_last_name'])
        ticket_text += " - PI Email: %s\n" % (data_list[1]['pi_email'])

        if data_list[2]['needs_spinal']:
            ticket_text += " User needs instrument access.  See below.\n"

        if data_list[2]['needs_storage']:
            ticket_text += " User needs network storage.  See below.\n"

        if data_list[2]['needs_other']:
            ticket_text += " User has other needs.  See below.\n"

        for k,v in data_list[3].iteritems():
            if v:
                ticket_text += " - %s: %s\n" % (k, v)

        tracker = rt.Rt(RT_URI, RT_USER, RT_PW)
        tracker.login()
        ticket_num = tracker.create_ticket(Queue='AccountRequest', Subject=subject_text, Text=ticket_text)
        tracker.logout()

        if ticket_num:
            request.rt_ticket_number = ticket_num
            request.save()

        return render_to_response('formtools/wizard/done.html', {'data_list': data_list},)

