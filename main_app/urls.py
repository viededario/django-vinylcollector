from django.urls import path
from .views import Home, VinylList, VinylDetail, GenreListCreate, GenreDetail# additional imports


from django.urls import path
from .views import Home, VinylList, VinylDetail, GenreListCreate, GenreDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # Routes for Vinyl CRUD operations
    path('vinyls/', VinylList.as_view(), name='vinyl-list'),
    path('vinyls/<int:id>/', VinylDetail.as_view(), name='vinyl-detail'),
    
    # New routes for Genre CRUD operations
    path('vinyls/<int:vinyl_id>/genres/', GenreListCreate.as_view(), name='genre-list-create'),
    path('vinyls/<int:vinyl_id>/genres/<int:id>/', GenreDetail.as_view(), name='genre-detail'),
]
