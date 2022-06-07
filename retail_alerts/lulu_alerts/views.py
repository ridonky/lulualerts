from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

# Create your views here.

# alerts = [{"name":"Define Jacket - Size S - Blue, Gray, + 5 more colors","type":"Price drop","dateset":"5/22/2022","status":"Active"},
#  {"name":"Scuba Hoodie - Size XS, S - Any colors","type":"Back in stock","dateset":"5/20/2022","status":"Notification sent 5/31/2022!"}]

class NewAlertForm(forms.Form):
    alert = forms.CharField(label = "Alert name")

# alerts = []

def index(request):
    return render(request, "lulu_alerts/index.html")

def products(request):
    return render(request, "lulu_alerts/products.html")

def login(request):
    return render(request, "lulu_alerts/login.html")

def signup(request):
    return render(request, "lulu_alerts/signup.html")

# logged in views

def newalert(request, alert_type):
    if request.method == "POST":
        form = NewAlertForm(request.POST)
        if form.is_valid():
            alert = form.cleaned_data["alert"]
            request.session["alerts"] += [{"name":alert,"type":alert_type,"dateset":"today","status":"active"}] # UM WOW KEEP THE BRACKETS OR ELSE!
            return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
        else:
            print("i was post, but didnt return a form")
            return render(request,"lulu_alerts/newalert.html", {
                "alert_type": alert_type,
                "form": form
            })

    return render(request, "lulu_alerts/newalert.html", {
        "alert_type": alert_type,
        "form": NewAlertForm()
    })

def myalerts(request):
    if "alerts" not in request.session:  # if there are no alerts, give them empty list.
        request.session["alerts"] = []

    return render(request, "lulu_alerts/myalerts.html", {
        "alerts": request.session["alerts"],
    })

# django stores session data in tables. 