from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from models import *

def home(request):
    return HttpResponse("You're home")

def index(request):
    return HttpResponse("You're looking at all requests.")

"""
def user_info(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = UserInfoForm()

    return render_to_response('contact.html', {
            'form': form,
            })

class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
                'form_data': [form.cleaned_data for form in form_list],
                })
"""
