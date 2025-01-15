
from django.contrib import admin
# import your models here
from .models import Vinyl, Genre, Track

# Register your models here
admin.site.register(Vinyl)
admin.site.register(Genre)
admin.site.register(Track)


