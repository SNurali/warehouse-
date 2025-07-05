from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import Company


class Warehouse(models.Model):
    WAREHOUSE_TYPES = (
        ('main', _('Main Warehouse')),
        ('regional', _('Regional Warehouse')),
        ('transit', _('Transit Point')),
        ('store', _('Store')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='warehouses',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=WAREHOUSE_TYPES,
        default='main'
    )
    address = models.TextField(_('Address'))
    contact_person = models.CharField(_('Contact Person'), max_length=100, blank=True)
    contact_phone = models.CharField(_('Contact Phone'), max_length=20, blank=True)
    contact_email = models.EmailField(_('Contact Email'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Location(models.Model):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('Warehouse')
    )
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20)
    aisle = models.CharField(_('Aisle'), max_length=10, blank=True)
    shelf = models.CharField(_('Shelf'), max_length=10, blank=True)
    bin = models.CharField(_('Bin'), max_length=10, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    capacity = models.DecimalField(
        _('Capacity'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        unique_together = ('warehouse', 'code')
        ordering = ['warehouse', 'aisle', 'shelf', 'bin']

    def __str__(self):
        return f"{self.warehouse.code} - {self.code}"


class ProductCategory(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='product_categories',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent Category')
    )
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    UNITS = (
        ('pc', _('Piece')),
        ('kg', _('Kilogram')),
        ('g', _('Gram')),
        ('l', _('Liter')),
        ('ml', _('Milliliter')),
        ('m', _('Meter')),
        ('cm', _('Centimeter')),
        ('box', _('Box')),
        ('pack', _('Pack')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=200)
    sku = models.CharField(_('SKU'), max_length=50, unique=True)
    barcode = models.CharField(_('Barcode'), max_length=50, blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Category')
    )
    unit = models.CharField(
        _('Unit'),
        max_length=10,
        choices=UNITS,
        default='pc'
    )
    description = models.TextField(_('Description'), blank=True)
    purchase_price = models.DecimalField(
        _('Purchase Price'),
        max_digits=12,
        decimal_places=2
    )
    selling_price = models.DecimalField(
        _('Selling Price'),
        max_digits=12,
        decimal_places=2
    )
    tax_rate = models.DecimalField(
        _('Tax Rate'),
        max_digits=5,
        decimal_places=2,
        default=0
    )
    min_stock = models.DecimalField(
        _('Minimum Stock'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    max_stock = models.DecimalField(
        _('Maximum Stock'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    weight = models.DecimalField(
        _('Weight'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    volume = models.DecimalField(
        _('Volume'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Inventory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name=_('Product')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name=_('Location')
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    reserved = models.DecimalField(
        _('Reserved'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    last_counted = models.DateTimeField(
        _('Last Counted'),
        null=True,
        blank=True
    )
    batch = models.CharField(
        _('Batch/Lot'),
        max_length=50,
        blank=True
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventory')
        unique_together = ('product', 'location', 'batch')

    def __str__(self):
        return f"{self.product} at {self.location}"


class Supplier(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='suppliers',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    contact_person = models.CharField(
        _('Contact Person'),
        max_length=100,
        blank=True
    )
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    address = models.TextField(_('Address'), blank=True)
    tax_id = models.CharField(_('Tax ID'), max_length=50, blank=True)
    payment_terms = models.CharField(
        _('Payment Terms'),
        max_length=100,
        blank=True
    )
    lead_time = models.IntegerField(
        _('Lead Time (days)'),
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('pending', _('Pending Approval')),
        ('approved', _('Approved')),
        ('ordered', _('Ordered')),
        ('partial', _('Partially Received')),
        ('received', _('Fully Received')),
        ('cancelled', _('Cancelled')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='purchase_orders',
        verbose_name=_('Company')
    )
    order_number = models.CharField(
        _('Order Number'),
        max_length=50,
        unique=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Supplier')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    order_date = models.DateField(_('Order Date'))
    expected_delivery = models.DateField(
        _('Expected Delivery'),
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)
    created_by = models.ForeignKey(
        'tenants.User',
        on_delete=models.PROTECT,
        related_name='created_purchase_orders',
        verbose_name=_('Created By')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.order_number} - {self.supplier}"


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Product')
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=2
    )
    unit_price = models.DecimalField(
        _('Unit Price'),
        max_digits=12,
        decimal_places=2
    )
    tax_rate = models.DecimalField(
        _('Tax Rate'),
        max_digits=5,
        decimal_places=2,
        default=0
    )
    received = models.DecimalField(
        _('Received'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        verbose_name=_('Destination Location'),
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Purchase Order Item')
        verbose_name_plural = _('Purchase Order Items')

    def __str__(self):
        return f"{self.order.order_number} - {self.product}"


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('purchase', _('Purchase')),
        ('sale', _('Sale')),
        ('transfer', _('Transfer')),
        ('adjustment', _('Adjustment')),
        ('return', _('Return')),
        ('production', _('Production')),
        ('consumption', _('Consumption')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='stock_movements',
        verbose_name=_('Company')
    )
    movement_type = models.CharField(
        _('Movement Type'),
        max_length=20,
        choices=MOVEMENT_TYPES
    )
    reference = models.CharField(
        _('Reference'),
        max_length=100,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='movements',
        verbose_name=_('Product')
    )
    from_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='outgoing_movements',
        verbose_name=_('From Location'),
        null=True,
        blank=True
    )
    to_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='incoming_movements',
        verbose_name=_('To Location'),
        null=True,
        blank=True
    )
    quantity = models.DecimalField(
        _('Quantity'),
        max_digits=10,
        decimal_places=2
    )
    batch = models.CharField(
        _('Batch/Lot'),
        max_length=50,
        blank=True
    )
    expiry_date = models.DateField(
        _('Expiry Date'),
        null=True,
        blank=True
    )
    date = models.DateTimeField(_('Date'))
    notes = models.TextField(_('Notes'), blank=True)
    created_by = models.ForeignKey(
        'tenants.User',
        on_delete=models.PROTECT,
        verbose_name=_('Created By')
    )

    class Meta:
        app_label = 'inventory'
        verbose_name = _('Stock Movement')
        verbose_name_plural = _('Stock Movements')
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product}"


class Transfer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='outgoing_transfers')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='incoming_transfers')
    reference = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('tenants.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"Transfer {self.reference} ({self.get_status_display()})"


class TransferItem(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'inventory'

    def __str__(self):
        return f"{self.product} x{self.quantity} (Transfer {self.transfer.reference})"