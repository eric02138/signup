from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from models import *
from forms import CaptchaForm

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

        request = Request()
        for form in data_list:
            for k,v in form.iteritems():
                request.set_attr(k, v)
        request.save()

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

        return render_to_response('formtools/wizard/done.html', {'data_list': data_list},)

