from django.db import models

from orders.models import Order
from packages.models import Package
from transfer.models import PlantTransfer
from users.models import CustomUser


class DeliveryNote(models.Model):
    delivery_note_number = models.IntegerField(unique=True)
    up = models.CharField(max_length=11)
    plant = models.CharField(max_length=11)
    package_type = models.ForeignKey(Package, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loading_date = models.DateField()
    unloading_date = models.DateField()
    package_count = models.IntegerField()
    total_height = models.FloatField()
    total_weight = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_notes')



    def __str__(self):
        return f'DeliveryNote #{self.delivery_note_number} ({self.up} → {self.plant})'