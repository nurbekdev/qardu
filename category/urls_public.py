from django.urls import path

from .views import CategoryAdminListView, StatisticsScientificView

app_name = "category_public"

urlpatterns = [
    path("list/", CategoryAdminListView.as_view(), name="list"),
    path("statistics/scientific/", StatisticsScientificView.as_view(), name="static"),
]
