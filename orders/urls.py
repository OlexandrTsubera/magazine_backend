from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.order_create, name='order_creates'),
    # path('orders/order_complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
