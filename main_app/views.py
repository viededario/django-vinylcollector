# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied # include this additional import

# additional imports below
from rest_framework import (
    generics,
    status,
    permissions,
)  # modify these imports to match
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Vinyl, Genre, Track
from .serializers import (
    VinylSerializer,
    GenreSerializer,
    TrackSerializer,
    UserSerializer,
)


# Define the home view
class Home(APIView):
    def get(self, request):
        content = {"message": "Welcome to the vinyl-collector api home route!"}
        return Response(content)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": response.data,
            }
        )


# User Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                }
            )
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# User Verification
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


class VinylList(generics.ListCreateAPIView):
    serializer_class = VinylSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Returns vinyls belonging to the logged-in user
        user = self.request.user
        return Vinyl.objects.filter(user=user)

    def perform_create(self, serializer):
        # Associates the newly created vinyl with the logged-in user
        serializer.save(user=self.request.user)


class VinylDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VinylSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restricts access to vinyls owned by the logged-in user
        user = self.request.user
        return Vinyl.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get tracks not associated with this vinyl
        tracks_not_associated = Track.objects.exclude(id__in=instance.tracks.all())
        tracks_serializer = TrackSerializer(tracks_not_associated, many=True)

        return Response({
            'vinyl': serializer.data,
            'tracks_not_associated': tracks_serializer.data
        })

    def perform_update(self, serializer):
        vinyl = self.get_object()
        if vinyl.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this vinyl."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this vinyl."})
        instance.delete()

class GenreListCreate(generics.ListCreateAPIView):
    serializer_class = GenreSerializer

    def get_queryset(self):
        vinyl_id = self.kwargs["vinyl_id"]
        return Genre.objects.filter(vinyl_id=vinyl_id)

    def perform_create(self, serializer):
        vinyl_id = self.kwargs["vinyl_id"]
        vinyl = Vinyl.objects.get(id=vinyl_id)
        serializer.save(vinyl=vinyl)


# View to retrieve, update, or delete a genre associated with a vinyl
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    lookup_field = "id"

    def get_queryset(self):
        vinyl_id = self.kwargs["vinyl_id"]
        return Genre.objects.filter(vinyl_id=vinyl_id)


class TrackListCreate(generics.ListCreateAPIView):
    # List all tracks or create a new track for a specific vinyl
    serializer_class = TrackSerializer

    def get_queryset(self):
        # Get all tracks for the given vinyl
        vinyl_id = self.kwargs["vinyl_id"]
        return Track.objects.filter(vinyl_id=vinyl_id)

    def perform_create(self, serializer):
        vinyl_id = self.kwargs["vinyl_id"]
        vinyl = Vinyl.objects.get(id=vinyl_id)  # Get the vinyl object
        serializer.save(vinyl=vinyl)  # Save track with the vinyl


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, or delete a specific track by its id
    serializer_class = TrackSerializer

    def get_queryset(self):
        # Return only tracks for the specific vinyl
        vinyl_id = self.kwargs["vinyl_id"]
        return Track.objects.filter(vinyl_id=vinyl_id)


class AddTrackToVinyl(generics.GenericAPIView):
    def post(self, request, vinyl_id, track_id):
        try:
            vinyl = Vinyl.objects.get(id=vinyl_id)
            track = Track.objects.get(id=track_id)

            # Add the track to the vinyl's tracks
            vinyl.tracks.add(track)
            vinyl.save()

            return Response(
                {"message": "Track added to vinyl successfully."},
                status=status.HTTP_200_OK,
            )
        except Vinyl.DoesNotExist:
            return Response(
                {"error": "Vinyl not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Track.DoesNotExist:
            return Response(
                {"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND
            )


class RemoveTrackFromVinyl(generics.GenericAPIView):
    def post(self, request, vinyl_id, track_id):
        try:
            vinyl = Vinyl.objects.get(id=vinyl_id)
            track = Track.objects.get(id=track_id)

            # Remove the track from the vinyl's tracks
            vinyl.tracks.remove(track)
            vinyl.save()

            return Response(
                {"message": "Track removed from vinyl successfully."},
                status=status.HTTP_200_OK,
            )
        except Vinyl.DoesNotExist:
            return Response(
                {"error": "Vinyl not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Track.DoesNotExist:
            return Response(
                {"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "Track is not associated with this vinyl."},
                status=status.HTTP_400_BAD_REQUEST,
            )
