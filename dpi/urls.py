from django.urls import path
from .views import *

#les urls de l'application dpi 
urlpatterns = [
      path('/ajouter_hopitaux' , ajouter_hopitaux),
      path('/creer_consultation' , creer_consultation) ,
      path('/ajouter_soin' , ajouter_soin)
]