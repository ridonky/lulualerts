from django.contrib import admin
from .models import Alert_Status, Products, Alerts, Alert_History

# Register your models here.
admin.site.register(Alert_Status)
admin.site.register(Products)
admin.site.register(Alerts)
admin.site.register(Alert_History)