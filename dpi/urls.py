from django.urls import path
from .views import *

#les urls de l'application dpi 
urlpatterns = [
      path('/ajouter-hopitaux' , ajouter_hopitaux),
      path('/creer-consultation' , creer_consultation) ,
      path('/ajouter-soin' , ajouter_soin),
      path('/ajouter-bilan-radiologique' , ajouter_Bilan_radiologique)
]