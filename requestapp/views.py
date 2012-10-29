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
        request = Request()
        for form in form_list:
            for k,v in form.cleaned_data.iteritems():
                request.set_attr(k, v)
        request.save()
            
        return render_to_response('formtools/wizard/done.html', {
                'form_data': [form.cleaned_data for form in form_list],
                })

