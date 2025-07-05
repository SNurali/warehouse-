from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from django import forms
from .models import (
    Warehouse, Location, Product, ProductCategory,
    Inventory, Supplier, PurchaseOrder, StockMovement
)
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib import messages
from django.db.models import F  # Добавьте этот импорт в начале файла
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Transfer, StockMovement
from .forms import TransferForm


class TransferListView(ListView):
    model = Transfer
    template_name = 'inventory/transfer_list.html'
    context_object_name = 'transfers'

    def get_queryset(self):
        return Transfer.objects.filter(
            from_warehouse__company=self.request.user.company
        ).select_related('from_warehouse', 'to_warehouse')


class TransferCreateView(CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'inventory/transfer_form.html'
    success_url = reverse_lazy('transfer_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TransferDetailView(DetailView):
    model = Transfer
    template_name = 'inventory/transfer_detail.html'
    context_object_name = 'transfer'


class TransferProcessView(DetailView):
    model = Transfer
    template_name = 'inventory/transfer_process.html'

    def post(self, request, *args, **kwargs):
        transfer = self.get_object()

        if transfer.status != 'pending':
            messages.warning(request, 'Transfer has already been processed')
            return redirect('transfer_detail', pk=transfer.pk)

        # Обработка перемещения товаров
        for item in transfer.items.all():
            # Проверка наличия товара на исходном складе
            from_inventory = Inventory.objects.filter(
                product=item.product,
                location__warehouse=transfer.from_warehouse
            ).first()

            if not from_inventory or from_inventory.quantity < item.quantity:
                messages.error(request,
                               f'Not enough stock for {item.product.name} in {transfer.from_warehouse.name}')
                return redirect('transfer_detail', pk=transfer.pk)

            # Списание с исходного склада
            from_inventory.quantity -= item.quantity
            from_inventory.save()

            # Поступление на целевой склад
            to_inventory, created = Inventory.objects.get_or_create(
                product=item.product,
                location__warehouse=transfer.to_warehouse,
                defaults={'quantity': 0}
            )
            to_inventory.quantity += item.quantity
            to_inventory.save()

            # Запись движения товара
            StockMovement.objects.create(
                product=item.product,
                from_location=from_inventory.location,
                to_location=to_inventory.location,
                quantity=item.quantity,
                movement_type='transfer',
                reference=transfer.reference,
                created_by=request.user
            )

        transfer.status = 'completed'
        transfer.save()

        messages.success(request, 'Transfer processed successfully')
        return redirect('transfer_detail', pk=transfer.pk)

# Форма для корректировки инвентаря
class InventoryAdjustForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    adjustment = forms.DecimalField(
        label='Adjustment Quantity',
        help_text='Use positive number to add, negative to subtract'
    )
    notes = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if company:
            self.fields['product'].queryset = Product.objects.filter(company=company)
            self.fields['location'].queryset = Location.objects.filter(warehouse__company=company)


# Warehouse Views
class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'


class WarehouseCreateView(CreateView):
    model = Warehouse
    fields = ['name', 'code', 'type', 'address', 'contact_person', 'contact_phone', 'contact_email', 'is_active']
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')


class WarehouseDetailView(DetailView):
    model = Warehouse
    template_name = 'inventory/warehouse_detail.html'


class WarehouseUpdateView(UpdateView):
    model = Warehouse
    fields = ['name', 'code', 'type', 'address', 'contact_person', 'contact_phone', 'contact_email', 'is_active']
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')


# Location Views
class LocationListView(ListView):
    model = Location
    template_name = 'inventory/location_list.html'


class LocationCreateView(CreateView):
    model = Location
    fields = ['warehouse', 'name', 'code', 'aisle', 'shelf', 'bin', 'is_active', 'capacity']
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('location_list')


class LocationDetailView(DetailView):
    model = Location
    template_name = 'inventory/location_detail.html'


class LocationUpdateView(UpdateView):
    model = Location
    fields = ['warehouse', 'name', 'code', 'aisle', 'shelf', 'bin', 'is_active', 'capacity']
    template_name = 'inventory/location_form.html'
    success_url = reverse_lazy('location_list')


# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'sku', 'barcode', 'category', 'unit', 'description',
              'purchase_price', 'selling_price', 'tax_rate',
              'min_stock', 'max_stock', 'weight', 'volume', 'is_active']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'sku', 'barcode', 'category', 'unit', 'description',
              'purchase_price', 'selling_price', 'tax_rate',
              'min_stock', 'max_stock', 'weight', 'volume', 'is_active']
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('product_list')


# Inventory Views
class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventory/inventory_list.html'


# Supplier Views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'


class SupplierCreateView(CreateView):
    model = Supplier
    fields = ['name', 'code', 'contact_person', 'phone', 'email', 'address',
              'tax_id', 'payment_terms', 'lead_time', 'is_active']
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'


class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ['name', 'code', 'contact_person', 'phone', 'email', 'address',
              'tax_id', 'payment_terms', 'lead_time', 'is_active']
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


# Purchase Order Views
class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'inventory/purchase_list.html'


class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    fields = ['order_number', 'supplier', 'status', 'order_date', 'expected_delivery', 'notes']
    template_name = 'inventory/purchase_form.html'
    success_url = reverse_lazy('purchase_list')


class PurchaseOrderDetailView(DetailView):
    model = PurchaseOrder
    template_name = 'inventory/purchase_detail.html'


class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    fields = ['order_number', 'supplier', 'status', 'order_date', 'expected_delivery', 'notes']
    template_name = 'inventory/purchase_form.html'
    success_url = reverse_lazy('purchase_list')


# Stock Movement Views
class StockMovementListView(ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'


class StockMovementDetailView(DetailView):
    model = StockMovement
    template_name = 'inventory/movement_detail.html'


# Inventory Adjustment View
class InventoryAdjustView(FormView):
    template_name = 'inventory/inventory_adjust.html'
    form_class = InventoryAdjustForm
    success_url = reverse_lazy('inventory_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        product = form.cleaned_data['product']
        location = form.cleaned_data['location']
        adjustment = form.cleaned_data['adjustment']
        notes = form.cleaned_data['notes']

        inventory, created = Inventory.objects.get_or_create(
            product=product,
            location=location,
            defaults={'quantity': 0}
        )

        inventory.quantity += adjustment
        inventory.save()

        StockMovement.objects.create(
            product=product,
            from_location=location if adjustment < 0 else None,
            to_location=location if adjustment > 0 else None,
            quantity=abs(adjustment),
            movement_type='adjustment',
            notes=notes,
            created_by=self.request.user
        )

        return super().form_valid(form)


class PurchaseReceiveView(DetailView):
    model = PurchaseOrder
    template_name = 'inventory/purchase_receive.html'

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        # Проверяем, что заказ не был уже полностью получен
        if order.status == 'received':
            messages.warning(request, 'This order has already been fully received')
            return redirect('purchase_detail', pk=order.pk)

        # Получаем все неполученные позиции заказа
        items_to_receive = order.items.filter(received__lt=F('quantity'))

        if not items_to_receive.exists():
            messages.warning(request, 'All items have already been received')
            return redirect('purchase_detail', pk=order.pk)

        # Помечаем позиции как полученные
        for item in items_to_receive:
            item.received = item.quantity
            item.save()

            # Создаем движение товара на склад
            StockMovement.objects.create(
                product=item.product,
                to_location=item.location,
                quantity=item.quantity,
                movement_type='purchase',
                reference=order.order_number,
                created_by=request.user
            )

        # Обновляем статус заказа
        if order.items.filter(received__lt=F('quantity')).exists():
            order.status = 'partial'
        else:
            order.status = 'received'
        order.save()

        messages.success(request, 'Items have been successfully received')
        return redirect('purchase_detail', pk=order.pk)