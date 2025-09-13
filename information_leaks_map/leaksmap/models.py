from django.db import models

class Breach(models.Model):
    service_name = models.CharField(max_length=255)
    breach_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.service_name} - {self.breach_date}"
