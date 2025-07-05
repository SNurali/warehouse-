from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'warehouses', views.WarehouseViewSet, basename='warehouse')
router.register(r'inventory', views.InventoryViewSet, basename='inventory')
router.register(r'sales-orders', views.SalesOrderViewSet, basename='salesorder')
router.register(r'sales-order-items', views.SalesOrderItemViewSet, basename='salesorderitem')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]