from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name = 'login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/shop_create/', views.CreateShopProfileView.as_view(), name='shop_profile_create'),
    path('profile/customer_create/', views.CreateCustomerProfileView.as_view(), name='customer_profile_create'),
    path('profile/customer/<int:pk>/', views.DetailCustomerProfileView.as_view(), name='customer_detail'),
    path('profile/shop/<int:pk>/', views.DetailShopProfileView.as_view(), name='shop_detail'),
]