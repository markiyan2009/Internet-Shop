from django.urls import path
from . import views

urlpatterns = [
    path('home/categories/', views.HomeCategoriesView.as_view(), name = 'home_categories'),
    path('order/update_status/<int:pk>/', views.UpdateOrderStatusView.as_view(), name = 'update_order_status'),
    path('products/', views.ProductShopListView.as_view(), name = 'shop_products'),
    path('orders/manager/<int:user_pk>/', views.OrderListManagerView.as_view(), name = 'orders_manager'),
    path('product/<int:pk>/', views.ShopProductView.as_view(), name = 'update_product'),
    path('product/discount/create/<int:pk>/', views.CreateDiscountView.as_view(), name = 'create_discount'),
    path('product/create/', views.create_product , name = 'create_product'),
    path('product/delete/<int:pk>/', views.DeleteProductView.as_view(), name = 'delete_product'),
]