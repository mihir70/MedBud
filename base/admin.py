from django.contrib import admin

# # Register your models here.

from .models import Imagine, Room, Topic, Message,  Prescription

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Prescription)
admin.site.register(Imagine)
