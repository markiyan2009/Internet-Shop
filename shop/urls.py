from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('home/categories/', views.HomeCategoriesView.as_view(), name = 'home_categories'),
    path('order/update_status/<int:pk>/', (cache_page(60*2))(views.UpdateOrderStatusView.as_view()), name = 'update_order_status'),
    path('products/', (cache_page(60*2))(views.ProductShopListView.as_view()), name = 'shop_products'),
    path('orders/manager/<int:user_pk>/', views.OrderListManagerView.as_view(), name = 'orders_manager'),
    path('product/<int:pk>/', (cache_page(60*2))(views.ShopProductView.as_view()), name = 'update_product'),
    path('product/discount/create/<int:pk>/', (cache_page(60*10))(views.CreateDiscountView.as_view()), name = 'create_discount'),
    path('product/create/', (cache_page(60*2))(views.create_product) , name = 'create_product'),
    path('product/delete/<int:pk>/', (cache_page(60*2))(views.DeleteProductView.as_view()), name = 'delete_product'),
]