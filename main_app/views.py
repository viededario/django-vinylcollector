# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

# additional imports below
from rest_framework import generics
from .models import Vinyl, Genre
from .serializers import VinylSerializer, GenreSerializer


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