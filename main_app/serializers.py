from rest_framework import serializers
from .models import Vinyl
from .models import Genre
from .models import Track
from django.contrib.auth.models import User  # add this line to list of imports


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data[
                "password"
            ],  # Ensures the password is hashed correctly
        )

        return user


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            "id",
            "title",
            "vinyl",
            "duration",
            "side",
            "position",
            "artist",
            "composer",
            "is_favorite",
            "notes",
        ]


class VinylSerializer(serializers.ModelSerializer):
    played_for_today = serializers.SerializerMethodField()  
    tracks = TrackSerializer(many=True, read_only=True)  
    user = serializers.PrimaryKeyRelatedField(read_only=True)  

    class Meta:
        model = Vinyl
        fields = '__all__'

    def get_played_for_today(self, obj):
        return obj.played_for_today()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        read_only_fields = ("vinyl",)
