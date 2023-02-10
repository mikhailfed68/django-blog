"""Users app URL Configuration."""

from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("", views.UserListView.as_view(), name="users"),
    path("register/", views.SiqnUp.as_view(), name="signup"),
    path("<username>", views.ProfileDetailView.as_view(), name="profile"),
    path("<username>/edit", views.UserUpdateView.as_view(), name="update_user"),
    path("<username>/delete", views.UserDestroyView.as_view(), name="destroy_user"),
    path("add_blog/", views.AddBlogToUserView.as_view(), name="add_blog_to_profile"),
    path("delete_blog/", views.RemoveBlogFromUserView.as_view(), name="delete_blog_from_profile"),
    path("add_author/", views.AddAuthorToProfileView.as_view(), name="add_author_to_profile"),
    path("remove_author/", views.RemoveAuthorFromProfileView.as_view(), name="remove_author_from_profile"),
]
