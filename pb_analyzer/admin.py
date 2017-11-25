from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Participant)
admin.site.register(ParticipantStats)
admin.site.register(ParticipantIdentity)
admin.site.register(ParticipantTimeline)
