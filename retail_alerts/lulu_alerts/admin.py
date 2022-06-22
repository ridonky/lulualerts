from django.contrib import admin
from .models import Alert_Status, Notif_Origin, Notif_Status, Notifications, Products, Alerts

# Register your models here.
admin.site.register(Alert_Status)
admin.site.register(Products)
admin.site.register(Alerts)
admin.site.register(Notif_Origin)
admin.site.register(Notif_Status)
admin.site.register(Notifications)

