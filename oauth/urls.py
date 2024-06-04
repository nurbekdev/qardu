from django.urls import path

from .views import login_view, logout_view, user_profile_view

app_name = "oauth"

urlpatterns = [
    path("profile/", user_profile_view, name="profile"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
