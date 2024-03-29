# Set up with django app settings
import os
import django

# can i make this setup conditional? IE: look for what the django settings module is then use it to import AUTH TOKEN
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_alerts.dev_settings')
from retail_alerts.dev_settings import AUTH_TOKEN

django.setup()

# Modules for django models, scraping, and sending notifs
from trycourier import Courier
from lulu_alerts.models import Alerts, Alert_Status, Notifications, Notif_Status
from time import sleep
from datetime import datetime
import requests
import json
from scripts.scrape import price, stock_status 

# Set up scheduler
#reference: https://github.com/agronholm/apscheduler/blob/3.x/examples/schedulers/background.py
from apscheduler.schedulers.background import BackgroundScheduler

# Check active alerts for trigger
def alerts_check():
    active = Alerts.objects.filter(status=1) 
    price_drop_alerts = active.filter(alert_type = "price_drop")
    back_in_stock_alerts = active.filter(alert_type = "back_in_stock")
    price_drop_check(price_drop_alerts)
    back_in_stock_check(back_in_stock_alerts)

def price_drop_check(alerts):
    price_drop_triggered_alerts = []
    for alert in alerts:
        url = alert.product.url
        # FOR NOW, dont confirm URL. Later validatieon:  url = confirm_url(url,alert.product)
        target_price = alert.target_price
        pricecheck = price(url)
        if pricecheck['currency'] == alert.product.currency:
            print(f'target_price is {target_price}')
            print(f"pricecheck['price'] is {pricecheck['price']}")
            if float(pricecheck['price']) <= target_price:
                # add to list & switch to triggered
                alert.status = Alert_Status.objects.get(id=2)
                alert.save()
                price_drop_triggered_alerts.append(alert)
            else:
                # check the next alert. or maybe shoudl check the next url
                print(f'no price drop for {alert}')
                continue
        else:
            # currency is wrong... handle this.
            pass
    notify('price_drop',price_drop_triggered_alerts)

def notify(alert_type,alerts):
    for alert in alerts: # HERE DO A TRY EXCEPT!
        new_notif=Notifications(alert=alert,status=Notif_Status.objects.get(id=1))
        new_notif.save()
        print('created new notif')
        if alert_type == "price_drop":
            print('sending notif')
            sendnotif = price_drop_notif(alert)
        elif alert_type == "back_in_stock":
            sendnotif = back_in_stock_notif(alert)
        if sendnotif == '':
            return False
        print(f"courier id is {sendnotif}") 
        new_notif.courier_response_id=sendnotif
        new_notif.save()
        print('updated courier req id')
        sleep(10)
        status = confirm_notif(new_notif.courier_response_id).lower()
        db_status = f"c_{status}"
        print('notif has complete status')
        new_notif.status=Notif_Status.objects.get(status=db_status)
        new_notif.complete_time = datetime.now() # this might be wrong??? warning: RuntimeWarning: DateTimeField Notifications.complete_time received a naive datetime (2022-06-23 19:09:53.961271) while time zone support is active.
        new_notif.save()
        print('notif complete time updated!')

def price_drop_notif(alert):
    client = Courier(auth_token=AUTH_TOKEN)
    resp = client.send_message(
      message={
        "to": {
          "email": alert.user.email,
        },
        "template": "YV95GRTJQS4VQVH2QATKPBVV4PDC",
        "data": {
          "firstName": alert.user.first_name,
          "name": alert.product.name,
          "color": alert.product.color,
          "target_price": str(alert.target_price), # should maybe use jsonencoder to convert decimal to str?
          "size": alert.product.size,
          "url": alert.product.url
        },
      }
    )
    response_id = resp['requestId']
    print(response_id)
    return response_id

def back_in_stock_check(alerts):
    back_in_stock_triggered_alerts = []
    print('checking bis alerts:')
    for alert in alerts:
        print(alert)
        url = alert.product.url
        if stock_status(url):
            alert.status = Alert_Status.objects.get(id=2)
            alert.save()
            back_in_stock_triggered_alerts.append(alert)
    notify('back_in_stock',back_in_stock_triggered_alerts)

def back_in_stock_notif(alert):
    client = Courier(auth_token=AUTH_TOKEN)
    print('sending back in stock notif')
    resp = client.send_message(
        message={
            "to": {
                "email":alert.user.email,
            },
            "template": "F73DGHK6MM4E9RPE7MSSNJAG9WGT",
            "data": {
                "firstName": alert.user.first_name,
                "name": alert.product.name,
                "color": alert.product.color,
                "size": alert.product.size,
                "url": alert.product.url
            }
        }
    )
    response_id = resp['requestId']
    print(response_id)
    return response_id

def confirm_notif(notif_response_id):
    url = (f"https://api.courier.com/messages/{notif_response_id}")
    headers = {
    "Accept": "application/json",
    "Authorization":f"Bearer {AUTH_TOKEN}"
    }
    response = requests.request("GET", url, headers=headers)
    status = json.loads(response.text)["status"]
    return status


def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(alerts_check,'interval',minutes=30)
    scheduler.start()
    



