from django.db import models
from django.conf import settings
from sqlalchemy import ForeignKey
# from django.contrib.auth.models import User

# Create your models here.
class Alert_Status(models.Model):
    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.status}"

class Products(models.Model):
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    price = models.IntegerField(blank=True)
    currency = models.CharField(max_length=6)
    url = models.URLField(max_length=200)
    in_stock = models.BooleanField() # added this new....

    def __str__(self):
        return f"{self.name} in {self.color}, size {self.size}"

class Alerts(models.Model):
    # id ??
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # or should this be on User ? as above?
    alert_type = models.CharField(max_length=20)
    status = models.ForeignKey(Alert_Status, on_delete=models.CASCADE)
    target_price = models.IntegerField(blank=True)
    date_set = models.DateField()
    alert_method = models.CharField(max_length=20, default="email")
    #double check this is how you do default?

    def __str__(self):
        return f"{self.alert_type} alert ID {self.id} for user {self.user_id}: currently {self.status}, set {self.date_set} for product {self.product_id}"

class Alert_History(models.Model):
    alert = models.ForeignKey(Alerts,on_delete=models.CASCADE)
    date_time_sent = models.DateTimeField()
    sent_method = models.CharField(max_length=20, default="email") 
        #  start off with just default types for now..

    def __str__(self):
        return f"Alert {self.alert} of type {self.sent_method} sent {self.date_time_sent}"