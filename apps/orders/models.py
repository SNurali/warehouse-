from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.tenants.models import Company
from apps.inventory.models import Product, Location


class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('individual', _('Individual')),
        ('business', _('Business')),
        ('government', _('Government')),
    )

    company = models.ForeignKey(
        'tenants.Company',
        on_delete=models.CASCADE,
        related_name='customers',
        verbose_name=_('Company')
    )
    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=CUSTOMER_TYPES,
        default='individual'
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
    credit_limit = models.DecimalField(
        _('Credit Limit'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class SalesOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('partial', _('Partially Shipped')),
        ('shipped', _('Fully Shipped')),
        ('invoiced', _('Invoiced')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='sales_orders',
        verbose_name=_('Company')
    )
    order_number = models.CharField(
        _('Order Number'),
        max_length=50,
        unique=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Customer')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    order_date = models.DateField(_('Order Date'))
    expected_shipment = models.DateField(
        _('Expected Shipment'),
        null=True,
        blank=True
    )
    shipping_address = models.TextField(
        _('Shipping Address'),
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)
    created_by = models.ForeignKey(
        'tenants.User',
        on_delete=models.PROTECT,
        related_name='created_sales_orders',
        verbose_name=_('Created By')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Sales Order')
        verbose_name_plural = _('Sales Orders')
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.order_number} - {self.customer}"


class SalesOrderItem(models.Model):
    order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order')
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='sales_order_items',
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
    shipped = models.DecimalField(
        _('Shipped'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    location = models.ForeignKey(
        'inventory.Location',
        on_delete=models.PROTECT,
        verbose_name=_('Source Location'),
        null=True,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        verbose_name = _('Sales Order Item')
        verbose_name_plural = _('Sales Order Items')

    def __str__(self):
        return f"{self.order.order_number} - {self.product}"


class Shipment(models.Model):
    STATUS_CHOICES = (
        ('preparing', _('Preparing')),
        ('ready', _('Ready to Ship')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='shipments',
        verbose_name=_('Company')
    )
    shipment_number = models.CharField(
        _('Shipment Number'),
        max_length=50,
        unique=True
    )
    order = models.ForeignKey(
        SalesOrder,
        on_delete=models.PROTECT,
        related_name='shipments',
        verbose_name=_('Order')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='preparing'
    )
    shipment_date = models.DateField(
        _('Shipment Date'),
        null=True,
        blank=True
    )
    tracking_number = models.CharField(
        _('Tracking Number'),
        max_length=100,
        blank=True
    )
    carrier = models.CharField(
        _('Carrier'),
        max_length=100,
        blank=True
    )
    notes = models.TextField(_('Notes'), blank=True)
    created_by = models.ForeignKey(
        'tenants.User',
        on_delete=models.PROTECT,
        verbose_name=_('Created By')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Shipment')
        verbose_name_plural = _('Shipments')
        ordering = ['-shipment_date']

    def __str__(self):
        return f"{self.shipment_number} - {self.order}"


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Shipment')
    )
    order_item = models.ForeignKey(
        SalesOrderItem,
        on_delete=models.PROTECT,
        related_name='shipment_items',
        verbose_name=_('Order Item')
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

    class Meta:
        verbose_name = _('Shipment Item')
        verbose_name_plural = _('Shipment Items')

    def __str__(self):
        return f"{self.shipment.shipment_number} - {self.order_item.product}"