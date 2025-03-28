from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Charities"

    def __str__(self):
        return self.name

