from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Customer, SalesOrder, Shipment
from .forms import CustomerForm, SalesOrderForm, ShipmentForm


# Customer Views
class CustomerListView(ListView):
    model = Customer
    template_name = 'orders/customer_list.html'

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'orders/customer_form.html'
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'orders/customer_detail.html'

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'orders/customer_form.html'
    success_url = reverse_lazy('customer_list')

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)


# Sales Order Views
class SalesOrderListView(ListView):
    model = SalesOrder
    template_name = 'orders/sales_list.html'

    def get_queryset(self):
        return SalesOrder.objects.filter(company=self.request.user.company)


class SalesOrderCreateView(CreateView):
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'orders/sales_form.html'
    success_url = reverse_lazy('sales_list')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SalesOrderDetailView(DetailView):
    model = SalesOrder
    template_name = 'orders/sales_detail.html'

    def get_queryset(self):
        return SalesOrder.objects.filter(company=self.request.user.company)


class SalesOrderUpdateView(UpdateView):
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'orders/sales_form.html'
    success_url = reverse_lazy('sales_list')

    def get_queryset(self):
        return SalesOrder.objects.filter(company=self.request.user.company)


class SalesOrderProcessView(DetailView):
    model = SalesOrder
    template_name = 'orders/sales_process.html'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        # Логика обработки заказа
        return redirect('sales_detail', pk=order.pk)


# Shipment Views
class ShipmentListView(ListView):
    model = Shipment
    template_name = 'orders/shipment_list.html'

    def get_queryset(self):
        return Shipment.objects.filter(order__company=self.request.user.company)


class ShipmentCreateView(CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'orders/shipment_form.html'
    success_url = reverse_lazy('shipment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs


class ShipmentDetailView(DetailView):
    model = Shipment
    template_name = 'orders/shipment_detail.html'

    def get_queryset(self):
        return Shipment.objects.filter(order__company=self.request.user.company)


class ShipmentUpdateView(UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'orders/shipment_form.html'
    success_url = reverse_lazy('shipment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs


class ShipmentProcessView(DetailView):
    model = Shipment
    template_name = 'orders/shipment_process.html'

    def post(self, request, *args, **kwargs):
        shipment = self.get_object()
        # Логика обработки отгрузки
        return redirect('shipment_detail', pk=shipment.pk)