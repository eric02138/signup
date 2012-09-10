from django.contrib import admin
from requestapp.models import RCUser, Service, Request

admin.site.register(RCUser)
admin.site.register(Service)
admin.site.register(Request)
