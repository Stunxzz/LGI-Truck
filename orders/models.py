from math import ceil
from django.db import models
from packages.models import Package


class Order(models.Model):
    status = models.IntegerField(default=0)
    up_user = models.CharField(max_length=100, default='151561')
    up = models.CharField(max_length=10)
    plant = models.CharField(max_length=10)
    loading_date = models.DateField()
    unloading_date = models.DateField()
    terms_of_delivery = models.CharField(max_length=100, default='FCA')
    packages_type = models.CharField(max_length=255)
    package_count = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    ldm = models.FloatField()

    def calculate_ldm(self):
        package = Package.objects.filter(type=self.packages_type).first()
        if not package:
            return
        ldm_height = ceil(self.height/package.max_height) * package.ldm
        ldm_weight = ceil(self.weight / package.max_weight) * package.ldm

        self.ldm = max(ldm_height, ldm_weight)
        self.save(update_fields=["ldm"])




    def __str__(self):
        return f"Order {self.id} - {self.up} ({self.loading_date})"


