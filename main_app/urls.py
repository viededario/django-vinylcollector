from django.urls import path
from .views import Home, VinylList, VinylDetail, GenreListCreate, GenreDetail, TrackListCreate, TrackDetail# additional imports


from django.urls import path
from .views import Home, VinylList, VinylDetail, GenreListCreate, GenreDetail, TrackListCreate, TrackDetail, AddTrackToVinyl, RemoveTrackFromVinyl

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # Routes for Vinyl CRUD operations
    path('vinyls/', VinylList.as_view(), name='vinyl-list'),
    path('vinyls/<int:id>/', VinylDetail.as_view(), name='vinyl-detail'),
    
    # New routes for Genre CRUD operations
    path('vinyls/<int:vinyl_id>/genres/', GenreListCreate.as_view(), name='genre-list-create'),
    path('vinyls/<int:vinyl_id>/genres/<int:id>/', GenreDetail.as_view(), name='genre-detail'),
    # Routes for Track CRUD operations
    path('vinyls/<int:vinyl_id>/tracks/', TrackListCreate.as_view(), name='track-list-create'),  
    path('vinyls/<int:vinyl_id>/tracks/<int:id>/', TrackDetail.as_view(), name='track-detail'),  
    path('vinyls/<int:vinyl_id>/add_track/<int:track_id>/', AddTrackToVinyl.as_view(), name='add-track-to-vinyl'),
    path('vinyls/<int:vinyl_id>/remove_track/<int:track_id>/', RemoveTrackFromVinyl.as_view(), name='remove-track-from-vinyl'),
]
