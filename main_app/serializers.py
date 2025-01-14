from rest_framework import serializers
from .models import Vinyl
from .models import Genre


class VinylSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinyl
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('vinyl',)