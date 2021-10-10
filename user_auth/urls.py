from django.urls import path
from .views import register,login_user,logout_view

app_name = "user_auth"
urlpatterns = [
    path("register/",register,name="sign-up"),
    path("login/",login_user,name="login"),
    path("logout",logout_view,name="logout")
]
