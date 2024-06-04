from django.urls import path

from .views import IndexPublicView

app_name = "index_public"

urlpatterns = [
    path("", IndexPublicView.as_view(), name="index"),
]
