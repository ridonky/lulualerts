from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.contrib import messages

from scripts.scrape import get_product_details
from django.contrib.auth.models import User
from lulu_alerts.models import Products, Alerts, Alert_Status
from scripts.alertscheck import run

# Create your views here.


class ProductQueryForm(forms.Form):
    productquery = forms.URLField(label="", label_suffix="")

class ConfigAlertForm(forms.Form):
    target_price = forms.DecimalField(label="Alert when price drops below")

# Test form - this is how you do a drop down!
class Test_form(forms.Form):
    EMAIL = 'EMAIL'
    METHOD_CHOICES = [
        (EMAIL, 'Email'),
    ]
    alert_method = forms.ChoiceField(
        choices = METHOD_CHOICES,
        error_messages={"required":"Text coming soon ;)"}
    )
# end test


# user signup form!
class CustomUserCreationForm(UserCreationForm):
    # firstname = forms.CharField(label='First name', max_length=30, required=True,widget=forms.TextInput(attrs={'class' : 'form-control'}))
    # email = forms.EmailField(label='Email address', help_text="Your email is required to recieve notifications. We'll never share it with anyone else.", required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(label='Password', 
        help_text='Your password must contain at least 8 characters.', 
        required=True, 
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', 
        help_text='Enter the same password as before, for verification.', 
        required=True, 
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("first_name", "email", "username", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def check_password_match(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(messages="Passwords don't match")
            return None
        return password1

    def check_valid_password(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            # raise forms.ValidationError(message="Password too short!~")
            return None
        return password

    def save(self, commit=True): 
        user = super(CustomUserCreationForm, self).save(commit=False) # what??
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password1']
        user.is_staff=False
        if commit:
            user.save()
        return user

    
# end new user signup form



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

# def signup(request):
#     return render(request, "lulu_alerts/signup.html")

# logged in views
def signup(request):
    if request.method == "POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            print('formisvalid')
            pw = form.check_password_match()
            if pw != form['password1']:
                print('pw didntmatch')
                # raise forms.ValidationError(message="Password must be at least 8 characters long.")
                return render(request, "lulu_alerts/signup.html",{"form":form, "messages":messages})
            elif form.check_valid_password() != pw:
                # messages = messages.error(request)
                print('pw not valid')
                return render(request, "lulu_alerts/sign_up.html",{"form":form})
            form.save()
            # messages = messages.success(request, 'Account created successfully')  
            return HttpResponseRedirect(reverse("lulu_alerts:myalerts"))
        # messages = messages.error(request,"Unsuccessful registration. Invalid information.")
        else:
            print('formisnotvalid')
    form = CustomUserCreationForm()
    return render(request,"lulu_alerts/signup.html",{"form": form, "messages":''})

# validate user and id access
def user_alert_id_permission(request,id):
    try:
        alert = Alerts.objects.get(id=id)
        if alert.user == request.user:
            return True
    except:
        Exception


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
                "form": Test_form()
            })

    else:
        return render(request,"lulu_alerts/newalert.html", {
            "product_form": ProductQueryForm(),
            "alert_config_form": ConfigAlertForm(),
            "alert_type": alert_type,
            "form": Test_form()
    })

@login_required
def view_alert(request,id):
    if user_alert_id_permission(request,id):
        alert = Alerts.objects.get(id=id)
        return render(request, "lulu_alerts/viewalert.html", 
        {"id":id,
        "alert":alert})
    else:
        return redirect("lulu_alerts:myalerts")
    # HttpResponse(f"Alert id is {id}")

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

run()


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