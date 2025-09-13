from django.db import models

class Breach(models.Model):
    service_name = models.CharField(max_length=255)
    breach_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.service_name} - {self.breach_date}"
