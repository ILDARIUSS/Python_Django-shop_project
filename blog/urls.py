from django.urls import path

from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),                 # /blogs/
    path("new/", BlogPostCreateView.as_view(), name="post_create"),         # /blogs/new/
    path("<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),    # /blogs/1/
    path("<int:pk>/edit/", BlogPostUpdateView.as_view(), name="post_edit"), # /blogs/1/edit/
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="post_delete"), # /blogs/1/delete/
]
