from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

alerts = [{"name":"Define Jacket - Size S - Blue, Gray, + 5 more colors","type":"Price drop","dateset":"5/22/2022","status":"Active"},
 {"name":"Scuba Hoodie - Size XS, S - Any colors","type":"Back in stock","dateset":"5/20/2022","status":"Notification sent 5/31/2022!"}]

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
    return render(request, "lulu_alerts/newalert.html", {
        "alert_type": alert_type
    })

def myalerts(request):
    return render(request, "lulu_alerts/myalerts.html", {
        "alerts": alerts
    })
