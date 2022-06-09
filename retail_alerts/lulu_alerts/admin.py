from django.contrib import admin
from .models import Alert_Config, Alert_Status, User_Alert_Map, Alerts_History

# Register your models here.
admin.site.register(Alert_Config)
admin.site.register(Alert_Status)
admin.site.register(User_Alert_Map)
admin.site.register(Alerts_History)