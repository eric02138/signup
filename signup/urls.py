from django.conf.urls import patterns, include, url
from requestapp.forms import (UserInfoForm, PIInfoForm, ServiceChoiceForm, 
                              SpinalResourceListForm, StorageChoiceForm, SoftwareChoiceForm, OtherForm)
from requestapp.views import RequestWizard, is_spinal_checked, is_storage_checked, is_software_checked, is_other_checked, captcha

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

multi_forms = [('userinfo', UserInfoForm), 
               ('piinfo', PIInfoForm), 
               ('servicechoices', ServiceChoiceForm), 
               ('spinalresources', SpinalResourceListForm),
               ('storage', StorageChoiceForm),
               ('softwarechoices', SoftwareChoiceForm), 
               ('otherinfo', OtherForm)]

urlpatterns = patterns('',
     url(r'^$', 'requestapp.views.home', name='home'),
     url(r'^requests/$', 'requestapp.views.index'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^request-wizard/$', RequestWizard.as_view(multi_forms, condition_dict={'spinalresources': is_spinal_checked,
                                                                          'storage': is_storage_checked,
                                                                          'softwarechoices': is_software_checked,
                                                                          'otherinfo': is_other_checked})),
    url(r'^request/$', captcha, name='captcha'),
    url(r'^request/pi-approval/(?P<id_md5>(\w){32})/(?P<approval_option_md5>(\w){32})/$', 'requestapp.views.pi_approval', name='pi_approval'),
)
