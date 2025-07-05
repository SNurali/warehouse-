# apps/api/serializers.py
from rest_framework import serializers
from django.utils import timezone
from django.db.models import Sum

# Import models using absolute paths
from apps.inventory.models import (
    Product,
    Warehouse,
    Location,
    ProductCategory,
    Inventory,
    Supplier,
    PurchaseOrder,
    PurchaseOrderItem,
    StockMovement,
    Transfer,
    TransferItem
)
from apps.orders.models import (
    Customer,
    SalesOrder,
    SalesOrderItem,
    Shipment,
    ShipmentItem
)


# ====================== Inventory Serializers ======================
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent', 'description', 'is_active']


class LocationSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'warehouse', 'warehouse_name', 'name', 'code',
            'aisle', 'shelf', 'bin', 'is_active', 'capacity', 'notes'
        ]


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'location', 'location_name', 'quantity', 'reserved',
            'batch', 'expiry_date', 'last_counted'
        ]


# ====================== Product Serializers ======================
class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source='category',
        write_only=True
    )
    in_stock = serializers.SerializerMethodField()
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'barcode', 'category', 'category_id',
            'unit', 'description', 'purchase_price', 'selling_price',
            'tax_rate', 'min_stock', 'max_stock', 'weight', 'volume',
            'is_active', 'created_at', 'updated_at', 'in_stock',
            'supplier', 'supplier_name', 'company'
        ]
        read_only_fields = ['created_at', 'updated_at', 'in_stock']

    def get_in_stock(self, obj):
        return Inventory.objects.filter(product=obj).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def validate_purchase_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Purchase price cannot be negative")
        return value

    def validate_selling_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Selling price cannot be negative")
        return value


# ====================== Warehouse Serializers ======================
class WarehouseSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            'id', 'company', 'company_name', 'name', 'code', 'type',
            'address', 'contact_person', 'contact_phone', 'contact_email',
            'is_active', 'notes', 'created_at', 'updated_at', 'locations',
            'total_items'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_items(self, obj):
        return Inventory.objects.filter(location__warehouse=obj).aggregate(
            total=Sum('quantity')
        )['total'] or 0


# ====================== Customer/Supplier Serializers ======================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'type', 'name', 'code', 'contact_person', 'phone',
            'email', 'address', 'tax_id', 'payment_terms', 'credit_limit',
            'notes', 'is_active', 'company'
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'code', 'contact_person', 'phone', 'email',
            'address', 'tax_id', 'payment_terms', 'lead_time', 'notes',
            'is_active', 'company'
        ]


# ====================== Purchase Order Serializers ======================
class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True, allow_null=True)

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'quantity',
            'unit_price', 'tax_rate', 'received', 'location', 'location_name',
            'notes'
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_number', 'supplier', 'supplier_name', 'status',
            'order_date', 'expected_delivery', 'notes', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'items',
            'total_amount', 'company'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_amount(self, obj):
        return obj.items.aggregate(
            total=Sum('quantity') * Sum('unit_price')
        )['total'] or 0


# ====================== Sales Order Serializers ======================
class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True, allow_null=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'quantity',
            'unit_price', 'tax_rate', 'shipped', 'location', 'location_name',
            'notes', 'total_price'
        ]

    def get_total_price(self, obj):
        return (obj.quantity * obj.unit_price) * (1 + obj.tax_rate / 100)


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'status',
            'order_date', 'expected_shipment', 'shipping_address', 'notes',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'items', 'total_amount', 'company'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_amount(self, obj):
        return sum(
            (item.quantity * item.unit_price) * (1 + item.tax_rate / 100)
            for item in obj.items.all()
        )


# ====================== Shipment Serializers ======================
class ShipmentItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='order_item.product.name', read_only=True)
    product_sku = serializers.CharField(source='order_item.product.sku', read_only=True)

    class Meta:
        model = ShipmentItem
        fields = [
            'id', 'order_item', 'product_name', 'product_sku', 'quantity',
            'batch', 'expiry_date'
        ]


class ShipmentSerializer(serializers.ModelSerializer):
    items = ShipmentItemSerializer(many=True, read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    customer_name = serializers.CharField(source='order.customer.name', read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id', 'shipment_number', 'order', 'order_number', 'status',
            'shipment_date', 'tracking_number', 'carrier', 'notes',
            'created_by', 'created_at', 'updated_at', 'items', 'customer_name'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ====================== Transfer Serializers ======================
class TransferItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = TransferItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity']


class TransferSerializer(serializers.ModelSerializer):
    items = TransferItemSerializer(many=True, read_only=True)
    from_warehouse_name = serializers.CharField(source='from_warehouse.name', read_only=True)
    to_warehouse_name = serializers.CharField(source='to_warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = Transfer
        fields = [
            'id', 'reference', 'from_warehouse', 'from_warehouse_name',
            'to_warehouse', 'to_warehouse_name', 'status', 'notes',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
            'items'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ====================== Stock Movement Serializer ======================
class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    from_location_name = serializers.CharField(source='from_location.name', read_only=True, allow_null=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True, allow_null=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'movement_type', 'reference', 'product', 'product_name',
            'product_sku', 'from_location', 'from_location_name',
            'to_location', 'to_location_name', 'quantity', 'batch',
            'expiry_date', 'date', 'notes', 'created_by', 'created_by_name',
            'company'
        ]