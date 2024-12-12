from django.urls import path
from .views import *

#les urls de l'application dpi 
urlpatterns = [
      path('/creer_consultation' , creer_consultation)
]