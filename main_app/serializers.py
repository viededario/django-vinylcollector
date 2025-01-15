from rest_framework import serializers
from .models import Vinyl
from .models import Genre
from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'vinyl', 'duration', 'side', 'position', 'artist', 'composer', 'is_favorite', 'notes']
class VinylSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True) 
    class Meta:
        model = Vinyl
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        read_only_fields = ('vinyl',)

