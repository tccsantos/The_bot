from django.db import models
from theme_manager.models import Theme
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Event(models.Model):

    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)
    month = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    year = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["month", "year"],
                name="unique_event_per_month_year",
            )
        ]
        ordering = ["-year", "-month"]
