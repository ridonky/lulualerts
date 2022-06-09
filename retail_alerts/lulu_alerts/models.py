from django.db import models
from django.conf import settings

# Create your models here.
class Alert_Status(models.Model):
    status = models.CharField(max_length=64)

class Alert_Config(models.Model):
    # id ??
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.ForeignKey(Alert_Status, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64)
    product_size = models.CharField(max_length=64, blank=True)
    product_color = models.CharField(max_length=64)
    url = models.URLField(max_length=200, blank=True)
    # sku??

    def __str__(self):
        return f"Alert {self.id} for {self.user}: {self.product_name}, size {self.product_size}, color {self.product_color}"

# i dont know if i need this class ...?
class User_Alert_Map(models.Model):
    alert = models.ForeignKey(Alert_Config, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Alerts_History(models.Model):
    alert = models.ForeignKey(Alert_Config,on_delete=models.CASCADE)
    time_sent = models.DateTimeField()
    type_sent = models.CharField(max_length=64, blank=True) 
        #  start off with no types for now..