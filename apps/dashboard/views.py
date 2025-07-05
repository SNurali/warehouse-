from django.views.generic import TemplateView
from inventory.models import Inventory
from orders.models import SalesOrder

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['low_stock'] = Inventory.objects.filter(
            quantity__lt=F('product__min_stock')
        )[:5]
        context['recent_orders'] = SalesOrder.objects.order_by('-created_at')[:5]
        return context