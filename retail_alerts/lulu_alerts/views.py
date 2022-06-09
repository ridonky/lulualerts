from click import pass_obj
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

# alerts = [{"name":"Define Jacket - Size S - Blue, Gray, + 5 more colors","type":"Price drop","dateset":"5/22/2022","status":"Active"},
#  {"name":"Scuba Hoodie - Size XS, S - Any colors","type":"Back in stock","dateset":"5/20/2022","status":"Notification sent 5/31/2022!"}]

class NewAlertForm(forms.Form):
    alert = forms.CharField(label="", label_suffix="")

# alerts = []

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
    if request.method == "POST":
        form = NewAlertForm(request.POST)
        if form.is_valid():
            alert = form.cleaned_data["alert"]
            dateset = date.today().isoformat()
            request.session["alerts"] += [{"name":alert,"type":alert_type,"dateset":dateset,"status":"active"}] # UM WOW KEEP THE BRACKETS OR ELSE!
            return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
        else:
            return render(request,"lulu_alerts/newalert.html", {
                "alert_type": alert_type,
                "form": form
            })

    return render(request, "lulu_alerts/newalert.html", {
        "alert_type": alert_type,
        "form": NewAlertForm()
    })

@login_required(login_url='lulu_alerts:login')
def myalerts(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("lulu_alerts:login"))
    #WOW the login_required decorator works instead of this!!!

    if "alerts" not in request.session:  # if there are no alerts, give them empty list.
        request.session["alerts"] = []

    return render(request, "lulu_alerts/myalerts.html", {
        "alerts": request.session["alerts"],
    })

# django stores session data in tables. 