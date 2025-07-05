from rest_framework import viewsets
from apps.inventory.models import Product, Warehouse, Inventory
from apps.orders.models import SalesOrder, SalesOrderItem
from apps.api.serializers import (
    ProductSerializer,
    WarehouseSerializer,
    InventorySerializer,
    SalesOrderSerializer,
    SalesOrderItemSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.none()  # Базовый queryset

    def get_queryset(self):
        return Product.objects.select_related(
            'company',
            'category',
            'supplier'
        ).prefetch_related(
            'inventory',
            'order_items',
            'movements'
        ).order_by('name')


class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.none()  # Базовый queryset

    def get_queryset(self):
        return Warehouse.objects.select_related(
            'company'
        ).prefetch_related(
            'locations',
            'incoming_transfers',
            'outgoing_transfers'
        ).order_by('name')


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.none()  # Базовый queryset

    def get_queryset(self):
        return Inventory.objects.select_related(
            'product',
            'location',
            'location__warehouse'
        ).order_by('product__name')


class SalesOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    queryset = SalesOrder.objects.none()  # Базовый queryset

    def get_queryset(self):
        return SalesOrder.objects.select_related(
            'company',
            'customer',
            'created_by'
        ).prefetch_related(
            'items',
            'shipments'
        ).order_by('-created_at')


class SalesOrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderItemSerializer
    queryset = SalesOrderItem.objects.none()  # Базовый queryset

    def get_queryset(self):
        return SalesOrderItem.objects.select_related(
            'order',
            'product',
            'location'
        ).order_by('order')