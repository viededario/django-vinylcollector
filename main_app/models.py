
from django.db import models

FORMATS = (
    ('LP', 'Long Play'),
    ('EP', 'Extended Play'),
    ('SG', 'Single'),
)

# Create your models here.
class Vinyl(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    release_date = models.DateField('Release Date')
    played_today = models.BooleanField(default=False)

    def played_for_today(self):
        # Checks if the vinyl has been played today
        return self.played_today

    def __str__(self):
        return self.name
class Genre(models.Model):
    name = models.CharField(max_length=100)  
    format = models.CharField(
        max_length=2,
        choices=FORMATS,
        default=FORMATS[0][0]
    )
    vinyl = models.ForeignKey('Vinyl', on_delete=models.CASCADE,  related_name='genres')

    def __str__(self):
        # Returns a friendly string representation of the genre
        return f"{self.get_format_display()} released on {self.vinyl.release_date}"

    class Meta:
        ordering = ['name']