from django.db import models



# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Completed'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
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


    def __str__(self):
        return f"Order {self.id} - {self.up} ({self.loading_date})"


