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
    path("following/", views.UserFollowingListView.as_view(), name="following"),
    path("add_author/", views.AddAuthorToProfileView.as_view(), name="add_author_to_profile"),
    path("remove_author/", views.RemoveAuthorFromProfileView.as_view(), name="remove_author_from_profile"),
    path("add_blog/", views.AddBlogToProfileView.as_view(), name="add_blog_to_profile"),
    path("remove_blog/", views.RemoveBlogFromProfileView.as_view(), name="remove_blog_from_profile"),
]
