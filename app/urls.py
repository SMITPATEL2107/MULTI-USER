from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.page,name="pge"),
    path("registeruser/",views.RegisterUser, name="registeruser"),
    path("loginpage/",views.LoginPage,name="loginpage"),
    path("loginuser",views.LoginUser,name="loginuser")
]
