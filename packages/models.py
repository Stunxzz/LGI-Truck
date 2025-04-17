from django.db import models

class Package(models.Model):
    type = models.CharField(max_length=50)
    ldm = models.FloatField()
    max_height = models.FloatField()
    max_weight = models.FloatField()

    def __str__(self):
        return self.type
