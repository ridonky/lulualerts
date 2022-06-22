from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Alert_Status(models.Model):
    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.status}"

class Products(models.Model):
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    price = models.DecimalField(blank=True,decimal_places=2,max_digits=5)
    currency = models.CharField(max_length=6)
    url = models.URLField(max_length=200)
    in_stock = models.BooleanField(default=True) # added this new....

    def __str__(self):
        return f"{self.name} in {self.color}, size {self.size}"

class Alerts(models.Model):
    # id ??
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # or should this be on User ? as above?
    alert_type = models.CharField(max_length=20)
    status = models.ForeignKey(Alert_Status, on_delete=models.CASCADE)
    target_price = models.DecimalField(blank=True,decimal_places=2,max_digits=5)
    date_set = models.DateField()
    alert_method = models.CharField(max_length=20, default="email")
    #double check this is how you do default?

    def __str__(self):
        return f"{self.alert_type} ID {self.id} for user {self.user_id}: currently {self.status}, set {self.date_set} for product {self.product_id}"

class Notif_Status(models.Model):
    status = models.CharField(max_length=20)
    # pending, sent, success, fail
    
    def __str__(self):
        return f"{self.id}: {self.status}"
    
class Notif_Origin(models.Model):
    origin = models.CharField(max_length=20)
    # original, retry, manual
    
    def __str__(self):
        return f"{self.id}: {self.origin}"
    
class Notifications(models.Model):
    alert = models.ForeignKey(Alerts, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    sent_time = models.DateTimeField(blank=True)
    complete_time = models.DateTimeField(blank=True)
    status = models.ForeignKey(Notif_Status, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, default="email")
    origin = models.ForeignKey(Notif_Origin, on_delete=models.CASCADE)
    # Do i get / store some sort of configmration ID from the email send request?


# class "Now"?
    # postgres specific: https://docs.djangoproject.com/en/4.0/ref/contrib/postgres/functions/#django.contrib.postgres.functions.TransactionNow
