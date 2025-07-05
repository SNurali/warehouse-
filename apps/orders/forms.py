from django import forms
from .models import Customer, SalesOrder, Shipment

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['type', 'name', 'code', 'contact_person', 'phone',
                 'email', 'address', 'tax_id', 'payment_terms',
                 'credit_limit', 'is_active']

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['order_number', 'customer', 'status', 'order_date',
                 'expected_shipment', 'shipping_address', 'notes']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if company:
            self.fields['customer'].queryset = Customer.objects.filter(company=company)

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['shipment_number', 'order', 'status', 'shipment_date',
                 'tracking_number', 'carrier', 'notes']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if company:
            self.fields['order'].queryset = SalesOrder.objects.filter(company=company)