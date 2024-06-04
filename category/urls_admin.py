from django.urls import path

from .views import CategoryAdminListView

app_name = "category_admin"

urlpatterns = [
    path("list/", CategoryAdminListView.as_view(), name="list"),
]
