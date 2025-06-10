from django.urls import path
from . import views

urlpatterns =[
    path('product/<int:pk>', views.ProductDetailView.as_view(), name = 'product'),
    path('basket/<int:pk>/', views.BusketDetailView.as_view(), name = 'basket_detail'),
    path('add_to_basket/<int:pk>', views.AddProductToBusketView.as_view(), name = 'add_product_to_basket'),
    path('create_order/', views.CreateOrderView.as_view(), name = 'create_order'), 
    path('orders/<int:user_pk>/', views.OrdersListView.as_view(), name = 'orders_list'),
    path('order/items/<int:order_pk>/', views.OrderItemsListView.as_view(), name = 'order_items_list'),
    path('review/add/<int:product_pk>/', views.CreateReviewView.as_view(), name = 'add_review'),
    path('product/review_add/<int:pk>/', views.PermCreateReviewView.as_view(), name = 'add_review_perm'),
    path('review/delete/<int:pk>/', views.DeleteReviewView.as_view(), name = 'delete_review'),
    path('basket/item/quantity_action/<int:pk>', views.ActionProductQuantityView.as_view(), name = 'action_quantity'),
    path('basket/item/delete/<int:pk>/', views.DeleteItemBusketView.as_view(), name='delete_item_basket'),
    path('order/cancel/<int:pk>/', views.CancelOrderView.as_view(), name = 'cancel_order'),
]