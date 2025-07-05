from django import forms
from .models import Product, Location
from django import forms
from .models import Transfer, TransferItem, Product, Warehouse

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


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['from_warehouse', 'to_warehouse', 'reference', 'notes']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if company:
            self.fields['from_warehouse'].queryset = Warehouse.objects.filter(company=company)
            self.fields['to_warehouse'].queryset = Warehouse.objects.filter(company=company)


class TransferItemForm(forms.ModelForm):
    class Meta:
        model = TransferItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)

        if company:
            self.fields['product'].queryset = Product.objects.filter(company=company)