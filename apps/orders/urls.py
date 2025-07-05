from django.urls import path
from .import views

urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),

    path('sales/', views.SalesOrderListView.as_view(), name='sales_list'),
    path('sales/add/', views.SalesOrderCreateView.as_view(), name='sales_add'),
    path('sales/<int:pk>/', views.SalesOrderDetailView.as_view(), name='sales_detail'),
    path('sales/<int:pk>/edit/', views.SalesOrderUpdateView.as_view(), name='sales_edit'),
    path('sales/<int:pk>/process/', views.SalesOrderProcessView.as_view(), name='sales_process'),

    path('shipments/', views.ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/add/', views.ShipmentCreateView.as_view(), name='shipment_add'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment_detail'),
    path('shipments/<int:pk>/edit/', views.ShipmentUpdateView.as_view(), name='shipment_edit'),
    path('shipments/<int:pk>/process/', views.ShipmentProcessView.as_view(), name='shipment_process'),
]