from django.urls import path
from . import views

app_name="lulu_alerts"
# so we can reference specific index page for lulu_alerts app

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("new_alert=<str:alert_type>", views.newalert, name="newalert"),
    path("myalerts", views.myalerts,name="myalerts")
]