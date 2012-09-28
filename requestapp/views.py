from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from models import *

def home(request):
    return HttpResponse("You're home")

def index(request):
    return HttpResponse("You're looking at all requests.")

def is_spinal_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('2') or {}
    return cleaned_data.get('needs_spinal', True)

def is_storage_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('2') or {}
    return cleaned_data.get('needs_storage', True)

def is_other_checked(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('2') or {}
    return cleaned_data.get('needs_other', True)

class RequestWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render_to_response('formtools/wizard/done.html', {
                'form_data': [form.cleaned_data for form in form_list],
                })

