from django.contrib import admin
from .models import Relay, RelaySlot, Certification

admin.site.register(Relay)
admin.site.register(RelaySlot)
admin.site.register(Certification)