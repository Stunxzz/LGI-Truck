from django.urls import path
from .views import OrderListView, UpdateOrderStatusView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('update-order-status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]
