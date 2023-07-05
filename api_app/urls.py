from django.urls import path
from api_app.views import cb_Login_User, cb_Signup_User, cb_User, cb_UserDetails, cb_UserDetails_all, cb_User_all

urlpatterns = [
    path("user/", cb_User),
    path("list_user", cb_User_all),
    path("login/", cb_Login_User),
    path("signup/", cb_Signup_User),
    path("user_details/", cb_UserDetails),
    path("list_user_details/", cb_UserDetails_all),
]

