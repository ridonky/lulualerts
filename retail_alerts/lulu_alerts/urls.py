from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name="lulu_alerts"
# so we can reference specific pages for lulu_alerts app

urlpatterns = [

    #path has 3 args: 
    # 1. what is the path/ route
    # 2. what do you want to render - from functions defined at views - at that path
    # 3. optinoally, represent the url pattern with a string name, to referencew)
    path("", views.index2, name="index2"),
    path("products", views.products, name="products"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("lulu_alerts/favicon.ico"))),
    path("myalerts/",views.myalerts,name="myalerts"),
    path("myalerts/<int:page>/",views.myalerts,name="myalerts"),
    path("myalerts/alert/<str:id>", views.view_alert, name="viewalert"),
    # path("new_alert=<alert_type>", views.newalert, name="newalert"), # OLD NEW ALERT!!!
    path("newalert=<alert_type>",views.newalertv2, name="newalertv2"),
    path("newalert/confirm_product",views.newalert_confirmproduct,name="newalert_confirmproduct"),
]