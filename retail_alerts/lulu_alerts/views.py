from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
import json

from flask import Config
from lulu_alerts.application import get_product_details
from django.contrib.auth.models import User
from lulu_alerts.models import Products, Alerts, Alert_Status

# Create your views here.


class ProductQueryForm(forms.Form):
    productquery = forms.URLField(label="", label_suffix="")

class ConfigAlertForm(forms.Form):
    target_price = forms.DecimalField(label="Alert when price drops below")


def index(request):
    return render(request, "lulu_alerts/index.html")

def products(request):
    return render(request, "lulu_alerts/products.html")

def login_view(request):
    if request.method == "GET":
        return render(request, "lulu_alerts/login.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST ["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
    
    return render(request, "lulu_alerts/login.html", {"message": "Invalid credentials"})

def signup(request):
    return render(request, "lulu_alerts/signup.html")

# logged in views

@login_required(login_url='lulu_alerts:login')
def logout_view(request):
    logout(request)
    return render(request, "lulu_alerts/login.html", {"message": "logged out."})

@login_required(login_url='lulu_alerts:login')
def newalert(request, alert_type):
    if request.method == "POST": # can i also check like a request id??  for actually submitting to DB
        if 'target_price' in request.POST:
            print(request.POST)
            target_price = request.POST['target_price']
            product = get_product_details(request.POST['url'])
            if target_price == "current_price":
                t_price = int(product["price"]) - .01
            else:
                t_price = request.POST['target_price_custom']
            p = Products.objects.create(name=product["name"], color=product["color"], size=product["size"], price=product["price"],url=product["url"],currency=product["currency"])
            p.save()
            u = User.objects.get(username = request.user)
            s = Alert_Status.objects.get(id=1)
            alert = Alerts.objects.create(product=p,user=u,alert_type=alert_type,status=s,target_price=t_price,date_set=date.today(),alert_method="email")
            alert.save()

            # fetch users list of alerts to pass them to my alerts!
            alerts = Alerts.objects.filter(user=u.id).order_by('-id')

            new_alert_message = "new alert created!"
            return render(request, "lulu_alerts/myalerts.html", {
                "new_alert_message":new_alert_message,
                "product": product,
                "alert_type": alert_type,
                "alerts": alerts
            })

        elif ProductQueryForm(request.POST):
            product_form = ProductQueryForm(request.POST)
            if product_form.is_valid():
                cleaned = product_form.cleaned_data
                print(f'form includes {cleaned["productquery"]}')
                product = get_product_details(cleaned["productquery"])
                return render(request,"lulu_alerts/newalert.html", {
                    "product": product,
                    "product_form": product_form,
                    "alert_type": alert_type,
                })
            else:
                return render(request,"lulu_alerts/newalert.html", {
                    "alert_type": alert_type,
                    "product_form": product_form,
                })
        else:
            return render(request, "lulu_alerts/newalert.html", {
                "product_form": product_form,
                "alert_type": alert_type,
            })

    else:
        return render(request,"lulu_alerts/newalert.html", {
            "product_form": ProductQueryForm(),
            "alert_config_form": ConfigAlertForm(),
            "alert_type": alert_type,
    })

@login_required
def product_query(request):
    if request.method == "POST":
        form = ProductQueryForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            print(cleaned["productquery"])
            return render(request,"lulu_alerts/product_query.html", {
                "product":get_product_details(cleaned["productquery"]),
                "form": form
            })
        else:
            return render(request, "lulu_alerts/product_query.html", {
                "form": form
            })

    else:
        return render(request,"lulu_alerts/product_query.html", {
        "form": ProductQueryForm()
    })

@login_required(login_url='lulu_alerts:login')
def myalerts(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("lulu_alerts:login"))
    #WOW the login_required decorator works instead of this!!!
    # u = User.objects.get(username=request.user)
    # alerts = Alerts.objects.filter(user=u.id)
    if 'alerts' not in request.GET or request.POST:
        u = User.objects.get(username=request.user)
        alerts = Alerts.objects.filter(user=u.id).order_by('-id')
        # if len(alerts) < 1:
        #     alerts = []

    return render(request, "lulu_alerts/myalerts.html", {
        "alerts": alerts,
    })

# django stores session data in tables. 






    # if request.method == "POST":
    #     form = NewAlertForm(request.POST)
    #     if form.is_valid():
    #         alert = form.cleaned_data["alert"]
    #         dateset = date.today().isoformat()
    #         request.session["alerts"] += [{"name":alert,"type":alert_type,"dateset":dateset,"status":"active"}] # UM WOW KEEP THE BRACKETS OR ELSE!
    #         return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
    #     else:
    #         return render(request,"lulu_alerts/newalert.html", {
    #             "alert_type": alert_type,
    #             "form": form
    #         })

    # return render(request, "lulu_alerts/newalert.html", {
    #     "alert_type": alert_type,
    #     "form": NewAlertForm()
    # })