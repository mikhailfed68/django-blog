from django.urls import path, include

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('register/', views.SiqnUp.as_view(), name='signup'),
    path('<username>', views.ProfileDetailView.as_view(), name='profile'),
]
