from django.contrib import admin
from requestapp.models import Request, InstrumentRequest, LabAdministrator

admin.site.register(Request)
admin.site.register(InstrumentRequest)
admin.site.register(LabAdministrator)
