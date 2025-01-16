from django.contrib import admin
from .models import BillingPeriod, Customer, Item, WithholdingTax, Factura

class BillingPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('identification', 'company', 'names', 'email', 'phone')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('code_reference', 'name', 'quantity', 'price', 'tax_rate')

class WithholdingTaxAdmin(admin.ModelAdmin):
    list_display = ('item', 'code', 'withholding_tax_rate')

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('reference_code', 'numbering_range_id', 'observation', 'payment_form', 'payment_due_date', 'payment_method_code')

admin.site.register(BillingPeriod, BillingPeriodAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(WithholdingTax, WithholdingTaxAdmin)
admin.site.register(Factura, FacturaAdmin)

