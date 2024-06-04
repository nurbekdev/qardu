from django.urls import include, path

urlpatterns = [
    path("categories/", include("api.v1.categories.urls")),
    path("departments/", include("api.v1.departments.urls")),
    path("users/", include("api.v1.users.urls")),
    path("posts/", include("api.v1.posts.urls")),
]
