from django.urls import path
from .views import (
    PostCreateView,
    PostDetailPublicView,
    PostListPublicView,
    PostOwnListPublicView,
    PostUpdateView,
    delete_post_view, # add this import if not already present
    PublishPostView, # add this import if not already present
)

app_name = "post_public"

urlpatterns = [
    path("list/", PostListPublicView.as_view(), name="list"),
    path("<int:pk>/", PostDetailPublicView.as_view(), name="detail"),
    path("mine/", PostOwnListPublicView.as_view(), name="my_list"),
    path("mine/create/", PostCreateView.as_view(), name="create"),
    path("mine/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("mine/<int:pk>/delete/", delete_post_view, name="delete"),  # Adding delete view
    path("mine/<int:pk>/publish/", PublishPostView.as_view(), name="publish"),  # Adding publish view
]
