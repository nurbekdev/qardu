from django.urls import include, path

urlpatterns = [
    path("", include("index.urls_admin")),
    path("kpi/", include("home.urls_admin")),
    path("categories/", include("category.urls_admin")),
    path("posts/", include("posts.urls_admin")),
]
