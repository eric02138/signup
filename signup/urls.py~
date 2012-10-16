from django.conf.urls import patterns, include, url
from requestapp.forms import UserInfoForm, PIInfoForm, ServiceChoiceForm, SpinalResourceListForm, StorageChoiceForm, OtherForm
from requestapp.views import RequestWizard, is_spinal_checked, is_storage_checked, is_other_checked

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

multi_forms = [('userinfo', UserInfoForm), 
               ('piinfo', PIInfoForm), 
               ('sericechoices', ServiceChoiceForm), 
               ('spinalresources', SpinalResourceListForm),
               ('storage', StorageChoiceForm),
               ('otherinfo', OtherForm)]

urlpatterns = patterns('',
     url(r'^$', 'requestapp.views.home', name='home'),
     url(r'^requests/$', 'requestapp.views.index'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^request/$', RequestWizard.as_view(multi_forms, condition_dict={'3': is_spinal_checked,
                                                                          '4': is_storage_checked,
                                                                          '5': is_other_checked})),
)
