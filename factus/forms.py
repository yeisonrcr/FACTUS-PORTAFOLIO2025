from django import forms
from .models import Factura, BillingPeriod, Customer, Item

INPUT_CLASSES = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-200 focus:border-blue-400 transition-colors"
SELECT_CLASSES = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-200 focus:border-blue-400 transition-colors"
TEXTAREA_CLASSES = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-200 focus:border-blue-400 transition-colors"

class BillingPeriodForm(forms.ModelForm):
    class Meta:
        model = BillingPeriod
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': INPUT_CLASSES
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': INPUT_CLASSES
            }),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['identification_document_id', 'identification', 'dv', 'company', 
                 'names', 'address', 'email', 'phone', 'legal_organization_id', 
                 'tribute_id', 'municipality_id']
        widgets = {
            'identification_document_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'identification': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'dv': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'company': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'names': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'address': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASSES}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'legal_organization_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'tribute_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'municipality_id': forms.Select(attrs={'class': SELECT_CLASSES}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code_reference', 'name', 'quantity', 'discount_rate', 'price', 
                 'tax_rate', 'unit_measure_id', 'standard_code_id', 'is_excluded', 
                 'tribute_id']
        widgets = {
            'code_reference': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'quantity': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'discount_rate': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'tax_rate': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
            'unit_measure_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'standard_code_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'is_excluded': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 shadow-sm focus:ring-2 focus:ring-blue-200 focus:border-blue-400 transition-colors'
            }),
            'tribute_id': forms.Select(attrs={'class': SELECT_CLASSES}),
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['numbering_range_id', 'reference_code', 'observation', 
                 'payment_form', 'payment_due_date', 'payment_method_code', 
                 'billing_period', 'customer', 'items']
        widgets = {
            'numbering_range_id': forms.Select(attrs={'class': SELECT_CLASSES}),
            'reference_code': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'observation': forms.Textarea(attrs={
                'class': TEXTAREA_CLASSES,
                'rows': '3'
            }),
            'payment_form': forms.Select(attrs={'class': SELECT_CLASSES}),
            'payment_due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': INPUT_CLASSES
            }),
            'payment_method_code': forms.Select(attrs={'class': SELECT_CLASSES}),
            'billing_period': forms.Select(attrs={'class': SELECT_CLASSES}),
            'customer': forms.Select(attrs={'class': SELECT_CLASSES}),
            'items': forms.SelectMultiple(attrs={'class': SELECT_CLASSES}),
        }