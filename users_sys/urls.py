from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('login/',views.LoginUserView.as_view(), name = 'login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/shop_create/', (cache_page(60*2))(views.CreateShopProfileView.as_view()), name='shop_profile_create'),
    path('profile/customer_create/', (cache_page(60*2))(views.CreateCustomerProfileView.as_view()), name='customer_profile_create'),
    path('profile/customer/<int:pk>/', (cache_page(60*2))(views.DetailCustomerProfileView.as_view()), name='customer_detail'),
    path('profile/shop/<int:pk>/', (cache_page(60*2))(views.DetailShopProfileView.as_view()), name='shop_detail'),
    path('profile/customer/update/<int:pk>/', (cache_page(60*2))(views.UpdateCustomerProfile.as_view()), name = 'update_customer_profile'),
    path('profile/shop/update/<int:pk>/', (cache_page(60*2))(views.UpdateShopProfile.as_view()), name = 'update_shop_profile'),
]