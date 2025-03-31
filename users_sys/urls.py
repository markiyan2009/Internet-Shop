from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.RegisterView.as_view(), name = 'register'),
    path('register/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]