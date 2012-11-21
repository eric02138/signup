from django.contrib import admin
from requestapp.models import Request, InstrumentRequest, LabAdministrator, Service, LabGroup

admin.site.register(Request)
admin.site.register(InstrumentRequest)
admin.site.register(LabAdministrator)
admin.site.register(Service)
admin.site.register(LabGroup)
