from django.contrib import admin
from requestapp.models import (Request, InstrumentRequest, LabAdministrator, Service, LabGroup,
                               RCUser, PIUser)

class LabGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'ad_group_name', 'members', 'services')

admin.site.register(Request)
admin.site.register(InstrumentRequest)
admin.site.register(LabAdministrator)
admin.site.register(Service)
admin.site.register(LabGroup)
admin.site.register(RCUser)
admin.site.register(PIUser)
