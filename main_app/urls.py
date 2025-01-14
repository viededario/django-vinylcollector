from django.urls import path
from .views import Home, VinylList, VinylDetail # additional imports


# import Home view from the views file
from .views import Home

urlpatterns = [
  path('', Home.as_view(), name='home'),
    # new routes below 
  path('vinyls/', VinylList.as_view(), name='vinyl-list'),
  path('vinyls/<int:id>/', VinylDetail.as_view(), name='vinyl-detail'),
]
