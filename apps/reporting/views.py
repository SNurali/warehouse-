from django.views.generic import ListView, TemplateView
from django.db.models import F  # Добавьте этот импорт
from apps.inventory.models import Product, Inventory, StockMovement  # Измените импорт
from apps.orders.models import SalesOrder  # Измените импорт

class ReportListView(TemplateView):
    template_name = 'reporting/report_list.html'

class InventoryReportView(ListView):
    template_name = 'reporting/inventory_report.html'
    model = Inventory
    context_object_name = 'inventory_items'

    def get_queryset(self):
        return self.model.objects.filter(
            location__warehouse__company=self.request.user.company
        ).select_related('product', 'location')

class SalesReportView(ListView):
    template_name = 'reporting/sales_report.html'
    model = SalesOrder
    context_object_name = 'sales_orders'

    def get_queryset(self):
        return self.model.objects.filter(
            company=self.request.user.company
        ).select_related('customer')

class PurchaseReportView(ListView):
    template_name = 'reporting/purchase_report.html'
    model = StockMovement
    context_object_name = 'purchases'

    def get_queryset(self):
        return self.model.objects.filter(
            movement_type='purchase',
            to_location__warehouse__company=self.request.user.company
        ).select_related('product', 'to_location')

class MovementReportView(ListView):
    template_name = 'reporting/movement_report.html'
    model = StockMovement
    context_object_name = 'movements'

    def get_queryset(self):
        return self.model.objects.filter(
            to_location__warehouse__company=self.request.user.company
        ).select_related('product', 'from_location', 'to_location')

class CustomReportView(TemplateView):
    template_name = 'reporting/custom_report.html'