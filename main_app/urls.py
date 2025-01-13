from django.urls import path

# import Home view from the views file
from .views import Home

urlpatterns = [
  path('', Home.as_view(), name='home'),
]
