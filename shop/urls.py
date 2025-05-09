from django.urls import path
from . import views

urlpatterns = [
    
    path('product/<int:pk>', views.ProductDetailView.as_view(), name = 'product'),
    path('basket/<int:pk>/', views.BusketDetailView.as_view(), name = 'basket_detail'),
    path('add_to_basket/<int:pk>', views.AddProductToBusketView.as_view(), name = 'add_product_to_basket'),
    path('create_order/', views.CreateOrderView.as_view(), name = 'create_order'), 
    path('orders/<int:user_pk>/', views.OrdersListView.as_view(), name = 'orders_list'),
    path('order/items/<int:order_pk>/', views.OrderItemsListView.as_view(), name = 'order_items_list'),
    path('order/update_status/<int:pk>/', views.UpdateOrderStatusView.as_view(), name = 'update_order_status'),
    path('review/add/<int:product_pk>/', views.CreateReviewView.as_view(), name = 'add_review'),
    path('orders/manager/<int:user_pk>/', views.OrderListManagerView.as_view(), name = 'orders_manager'),
]