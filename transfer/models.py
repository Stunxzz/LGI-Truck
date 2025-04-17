from django.db import models

class PlantTransfer(models.Model):
    up = models.CharField(max_length=11, unique=True)
    plant = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.up}'

