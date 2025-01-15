# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

# additional imports below
from rest_framework import generics
from .models import Vinyl, Genre, Track
from .serializers import VinylSerializer, GenreSerializer, TrackSerializer


# Define the home view
class Home(APIView):
    def get(self, request):
        content = {"message": "Welcome to the vinyl-collector api home route!"}
        return Response(content)


class VinylList(generics.ListCreateAPIView):
    queryset = Vinyl.objects.all()
    serializer_class = VinylSerializer


class VinylDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vinyl.objects.all()
    serializer_class = VinylSerializer
    lookup_field = "id"

    # Override the retrieve method
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get the list of tracks not associated with this vinyl
        tracks_not_associated = Track.objects.exclude(id__in=instance.tracks.all())
        tracks_serializer = TrackSerializer(tracks_not_associated, many=True)

        return Response({
            'vinyl': serializer.data,
            'tracks_not_associated': tracks_serializer.data
        })

class GenreListCreate(generics.ListCreateAPIView):
    serializer_class = GenreSerializer

    def get_queryset(self):
        vinyl_id = self.kwargs['vinyl_id']
        return Genre.objects.filter(vinyl_id=vinyl_id)

    def perform_create(self, serializer):
        vinyl_id = self.kwargs['vinyl_id']
        vinyl = Vinyl.objects.get(id=vinyl_id)
        serializer.save(vinyl=vinyl)


# View to retrieve, update, or delete a genre associated with a vinyl
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GenreSerializer
    lookup_field = 'id'

    def get_queryset(self):
        vinyl_id = self.kwargs['vinyl_id']
        return Genre.objects.filter(vinyl_id=vinyl_id)

class TrackListCreate(generics.ListCreateAPIView):
    # List all tracks or create a new track for a specific vinyl
    serializer_class = TrackSerializer

    def get_queryset(self):
        # Get all tracks for the given vinyl
        vinyl_id = self.kwargs['vinyl_id']
        return Track.objects.filter(vinyl_id=vinyl_id)

    def perform_create(self, serializer):
        vinyl_id = self.kwargs['vinyl_id']
        vinyl = Vinyl.objects.get(id=vinyl_id)  # Get the vinyl object
        serializer.save(vinyl=vinyl)  # Save track with the vinyl
        

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, or delete a specific track by its id
    serializer_class = TrackSerializer

    def get_queryset(self):
        # Return only tracks for the specific vinyl
        vinyl_id = self.kwargs['vinyl_id']
        return Track.objects.filter(vinyl_id=vinyl_id)


class AddTrackToVinyl(generics.GenericAPIView):
    def post(self, request, vinyl_id, track_id):
        try:
            vinyl = Vinyl.objects.get(id=vinyl_id)
            track = Track.objects.get(id=track_id)

            # Add the track to the vinyl's tracks
            vinyl.tracks.add(track)
            vinyl.save()

            return Response({"message": "Track added to vinyl successfully."}, status=status.HTTP_200_OK)
        except Vinyl.DoesNotExist:
            return Response({"error": "Vinyl not found."}, status=status.HTTP_404_NOT_FOUND)
        except Track.DoesNotExist:
            return Response({"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND)

class RemoveTrackFromVinyl(generics.GenericAPIView):
    def post(self, request, vinyl_id, track_id):
        try:
            vinyl = Vinyl.objects.get(id=vinyl_id)
            track = Track.objects.get(id=track_id)

            # Remove the track from the vinyl's tracks
            vinyl.tracks.remove(track)
            vinyl.save()

            return Response({"message": "Track removed from vinyl successfully."}, status=status.HTTP_200_OK)
        except Vinyl.DoesNotExist:
            return Response({"error": "Vinyl not found."}, status=status.HTTP_404_NOT_FOUND)
        except Track.DoesNotExist:
            return Response({"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Track is not associated with this vinyl."}, status=status.HTTP_400_BAD_REQUEST)