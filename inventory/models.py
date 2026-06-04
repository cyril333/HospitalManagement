from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class InventoryMedicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    expiry_date = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inventory_medicine'
        ordering = ['medicine_name']

    def __str__(self):
        return self.medicine_name

    def clean(self):
        errors = {}
        if self.quantity is not None and self.quantity < 0:
            errors['quantity'] = 'Quantity cannot be less than zero.'
        if self.unit_price is not None and self.unit_price < 0:
            errors['unit_price'] = 'Unit price cannot be negative.'
        if errors:
            raise ValidationError(errors)

    @property
    def stock_status(self):
        if self.quantity <= 0:
            return 'Out of Stock'
        if self.quantity < 10:
            return 'Low Stock'
        return 'In Stock'

    @property
    def expiry_status(self):
        if not self.expiry_date:
            return 'No Expiry'
        today = timezone.localdate()
        if self.expiry_date < today:
            return 'Expired'
        if (self.expiry_date - today).days <= 30:
            return 'Expiring Soon'
        return 'Valid'


class Supplies(models.Model):
    supply_id = models.AutoField(primary_key=True)
    supply_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    expiry_date = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'supplies'
        ordering = ['supply_name']

    def __str__(self):
        return self.supply_name

    def clean(self):
        errors = {}
        if self.quantity is not None and self.quantity < 0:
            errors['quantity'] = 'Quantity cannot be less than zero.'
        if self.unit_price is not None and self.unit_price < 0:
            errors['unit_price'] = 'Unit price cannot be negative.'
        if errors:
            raise ValidationError(errors)

    @property
    def stock_status(self):
        if self.quantity <= 0:
            return 'Out of Stock'
        if self.quantity < 10:
            return 'Low Stock'
        return 'In Stock'

    @property
    def expiry_status(self):
        if not self.expiry_date:
            return 'No Expiry'
        today = timezone.localdate()
        if self.expiry_date < today:
            return 'Expired'
        if (self.expiry_date - today).days <= 30:
            return 'Expiring Soon'
        return 'Valid'