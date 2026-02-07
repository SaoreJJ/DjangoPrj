
from django.urls import path
from .views import RegisterView, UserLoginView, UserLogoutView, ProfileView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),  # дополнительное
]