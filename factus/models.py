from django.db import models

class BillingPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

class Customer(models.Model):
    identification_document_id = models.CharField(max_length=100)
    identification = models.CharField(max_length=100)
    dv = models.IntegerField(null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    names = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    legal_organization_id = models.IntegerField()
    tribute_id = models.IntegerField()
    municipality_id = models.IntegerField(null=True, blank=True)

class Item(models.Model):
    code_reference = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    discount_rate = models.FloatField()
    price = models.FloatField()
    tax_rate = models.CharField(max_length=10)
    unit_measure_id = models.IntegerField()
    standard_code_id = models.IntegerField()
    is_excluded = models.IntegerField()
    tribute_id = models.IntegerField()

class WithholdingTax(models.Model):
    item = models.ForeignKey(Item, related_name='withholding_taxes', on_delete=models.CASCADE)
    code = models.IntegerField()
    withholding_tax_rate = models.IntegerField()

class Factura(models.Model):
    numbering_range_id = models.IntegerField(null=True, blank=True)
    reference_code = models.CharField(max_length=100, unique=True)
    observation = models.CharField(max_length=250, null=True, blank=True)
    payment_form = models.IntegerField(default=1)
    payment_due_date = models.DateField(null=True, blank=True)
    payment_method_code = models.IntegerField(default=10)
    billing_period = models.OneToOneField(BillingPeriod, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
