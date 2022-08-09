from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date

from scripts.scrape import get_product_details, get_photo
from django.contrib.auth.models import User
from lulu_alerts.models import Products, Alerts, Alert_Status
from scripts.alertscheck import run

# Create your views here.

# Form for product URL
class ProductQueryForm(forms.Form):
    productquery = forms.URLField(
        label="", 
        label_suffix="", 
        help_text="Remember to select your size and color at lululemon.com",
        widget=forms.URLInput(attrs={"class":"form-control", "autofocus":"autofocus", "placeholder":"https://shop.lululemon.com/..."}))

# Form for user signup
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', 
        help_text='Your password must contain at least 8 characters.',
        min_length=8, 
        required=True, 
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', 
        help_text='Enter the same password as before, for verification.', 
        required=True, 
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    usd_currency = 'USD'
    cad_currency = 'CAD'
    choices = [
        (usd_currency, 'USD'),
        (cad_currency, 'CAD')
    ]

    country = forms.ChoiceField(label='Choose currency',
        choices = choices,
        required=True,
        error_messages={"required":"Please select a currency."},
        widget=forms.Select(attrs={'class':'form-select'}),
    )

    class Meta:
        model = User
        fields = ("first_name", "email", "username", "country", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', "autofocus":"autofocus", 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
        }

    def check_password_match(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            return False
        return True

    def save(self, commit=True): 
        user = super(CustomUserCreationForm, self).save(commit=False) # what??
        if commit:
            user.save()
        print(user)
        return user


def index2(request):
    return render(request, "lulu_alerts/index2.html")

def products(request):
    return render(request, "lulu_alerts/products.html")

def login_view(request):
    if request.method == "GET":
        return render(request, "lulu_alerts/login.html")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST ["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
    
    return render(request, "lulu_alerts/login.html", {"message": "Invalid credentials"})

def signup(request):
    if request.method == "POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            print('formisvalid')
            print(form.cleaned_data)        
            form.save()
            username = form.cleaned_data["username"]
            print(username)
            password = form.cleaned_data["password1"]
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
            elif not form.check_password_match():
                message=("Passwords must match.")
                return render(request,"lulu_alerts/signup.html", {
                    "form":form,
                    "message":message
                })
        else:
            message = form.errors.as_text()
            return render(request, "lulu_alerts/signup.html", {
                "form":form,
                "message":message
                })
    form = CustomUserCreationForm()
    return render(request,"lulu_alerts/signup.html",{"form": form})

# validate user and id access
def user_alert_id_permission(request,id):
    try:
        alert = Alerts.objects.get(id=id)
        if alert.user == request.user:
            return True
    except:
        Exception

# logged in views
@login_required(login_url='lulu_alerts:login')
def logout_view(request):
    logout(request)
    return render(request, "lulu_alerts/login.html", {"message": "logged out."})

@login_required(login_url='lulu_alerts:login')
def newalert(request, alert_type):
    if request.method == "POST":
        if 'target_price' in request.POST:
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
                "form": Test_form()
            })

    else:
        return render(request,"lulu_alerts/newalert.html", {
            "product_form": ProductQueryForm(),
            # "alert_config_form": ConfigAlertForm(),
            "alert_type": alert_type,
            "form": Test_form()
    })


def lulu_url_check(url):
    # check if its a lulu url
    if 'mirror.co' in str(url):
        error = "lulualerts does not work for mirror products at this time"
        return error
    if 'lululemon' not in str(url):
        error = "URL must be be a lululemon product link"
        return error
    return True

@login_required(login_url='lulu_alerts:login')
def newalertv2(request,alert_type):
    if ProductQueryForm(request.POST):
        product_form = ProductQueryForm(request.POST)
        if product_form.is_valid():
            url = product_form.cleaned_data['productquery']
            if lulu_url_check(url) == True:
                product = get_product_details(url)
                print("attempting to render next page")
                request.session['product']=product # store it in the session instead of requiring args for now...
                request.session['alert_type']=alert_type
                request.session['url']=url
                return HttpResponseRedirect(reverse("lulu_alerts:newalert_confirmproduct"))
            else:
                error = lulu_url_check(url)
                return render(request,"lulu_alerts/newalert_v2.html",{
                "product_form":product_form,
                "alert_type":alert_type,
                "error":error
            })
        else: #form is not valid, give them whats there. - it may not have been a lulu URL!
            print("fucking invalid form")
            return render(request,"lulu_alerts/newalert_v2.html",{
                "product_form":product_form,
                "alert_type":alert_type,
            })
    print("treating it like a get req")
    return render(request, "lulu_alerts/newalert_v2.html", {
        "product_form": ProductQueryForm(),
        "alert_type": alert_type,
    })


@login_required(login_url='lulu_alerts:login')
def newalert_confirmproduct(request): 
    product = request.session['product']
    url = request.session['url']
    alert_type = request.session['alert_type']
    photo = get_photo(url)
    print(photo)
    if request.method == "POST":
        # for a price drop alert with a target price:
        price=request.POST["price"]
        if alert_type == 'price_drop':
            target_price = request.POST['target_price']
            if target_price == "current_price":
                t_price = int(price) - .01
            else:
                t_price = request.POST['target_price_custom']
        elif alert_type == 'back_in_stock':
            t_price = 0

        p = Products.objects.create(name=request.POST['product_name'], color=request.POST['color'], size=request.POST["size"], price=price,url=request.POST["url"],currency=request.POST["currency"],in_stock=product['in_stock'])
        p.save()
        u = User.objects.get(username = request.user)
        s = Alert_Status.objects.get(id=1)
        alert = Alerts.objects.create(product=p,user=u,alert_type=alert_type,status=s,target_price=t_price,date_set=date.today(),alert_method="email")
        alert.save()

        # fetch users list of alerts to pass them to my alerts!
        alerts = Alerts.objects.filter(user=u.id).order_by('-id')

        new_alert_message = "new alert created!"
        return render(request, "lulu_alerts/myalerts.html", {
            # alert message to make it nice and confirmy
            "new_alert_message":new_alert_message,
            # do we need alert type???
            "alert_type": alert_type, 
            "alerts": alerts,
        })
    return render(request,"lulu_alerts/newalert_confirmproduct.html", {
        "product":product,
        "url":url,
        "alert_type":alert_type,
        "photo": photo
    })

@login_required(login_url='lulu_alerts:login')
def view_alert(request,id):
    if request.method == "POST":
        a = Alerts.objects.get(id=id)
        Products.objects.get(id=a.product.id).delete()
        a.delete()
        return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
    if user_alert_id_permission(request,id):
        alert = Alerts.objects.get(id=id)
        return render(request, "lulu_alerts/viewalert.html", 
        {"id":id,
        "alert":alert})
    else:
        return redirect("lulu_alerts:myalerts")

@login_required(login_url='lulu_alerts:login')
def myalerts(request,page=1):
    # pull user and alerts
    u = User.objects.get(username=request.user)
    alert_list = Alerts.objects.filter(user=u.id).order_by('-id')
    # 5 per page
    p = Paginator(alert_list,5)
    page_object = p.get_page(page)
    
    return render(request, "lulu_alerts/myalerts.html", {
        "alerts":page_object,
        "p":p
    })

run()


# django stores session data in tables. 
