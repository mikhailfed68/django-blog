from django.urls import path, include

from users import views

app_name = 'users'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.signup, name='signup')
]
