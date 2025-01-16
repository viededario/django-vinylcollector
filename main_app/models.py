
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


FORMATS = (
    ('LP', 'Long Play'),
    ('EP', 'Extended Play'),
    ('SG', 'Single'),
)

SIDES = (
    ('A', 'Side A'),
    ('B', 'Side B'),
    ('C', 'Side C'),
    ('D', 'Side D'),
)

class Track(models.Model):
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=5, help_text="Duration in format MM:SS")  
    side = models.CharField(
        max_length=1,
        choices=SIDES,
        default=SIDES[0][0]
    )
    position = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Track number on the side"
    )
    artist = models.CharField(max_length=200, blank=True)  
    composer = models.CharField(max_length=200, blank=True)
    is_favorite = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.side}{self.position})"

    class Meta:
        ordering = ['vinyl', 'side', 'position']

# Create your models here.
class Vinyl(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    release_date = models.DateField('Release Date')
    played_today = models.BooleanField(default=False)
    tracks = models.ManyToManyField(Track)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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



