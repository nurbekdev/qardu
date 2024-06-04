from django.urls import path

from .views import IndexAdminView

app_name = "index_admin"

urlpatterns = [
    path("", IndexAdminView.as_view(), name="index"),
]
