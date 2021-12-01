from django.urls import path,include
from .views import (
    create_user,
    login_user,
    logout_user,
    password_reset,
    profile,
    password_change,
    dashboard,
    view_paper,
    verify_otp,
    resend_otp,
    reset_password,
    change_password
)

app_name = "user_auth"
urlpatterns = [
    path("login/",login_user,name="login"),
    path('signup/',create_user,name='signup'),
    path('logout/',logout_user,name='logout'),
    path("reset/",password_reset,name="password_reset"),
    path("profile/",profile,name="profile"),
    path("change_pass/",password_change,name="password_change"),
    path("dashboard/",dashboard,name="dashboard"),
    path("dashboard/paper/<int:title_id>/",view_paper,name="view-paper"),
    path("verify/",verify_otp,name="verify"),
    path("resend/<str:some>/",resend_otp,name="resend_otp"),
    path("reset_pass/",reset_password,name="reset_pass"),
    path("change_password/",change_password,name="change-pass"),
]
