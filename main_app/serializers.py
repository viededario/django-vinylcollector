from rest_framework import serializers
from .models import Vinyl

class VinylSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinyl
        fields = '__all__'
