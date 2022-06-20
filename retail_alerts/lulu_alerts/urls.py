from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name="lulu_alerts"
# so we can reference specific index page for lulu_alerts app

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("new_alert=<alert_type>", views.newalert, name="newalert"),
    path("myalerts", views.myalerts,name="myalerts"),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("img/favicon.ico")))
]