# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

# additional imports below
from rest_framework import generics
from .models import Vinyl
from .serializers import VinylSerializer


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
