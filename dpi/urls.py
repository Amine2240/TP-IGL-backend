from django.urls import path
from .views import *

#les urls de l'application dpi 
urlpatterns = [
      path('/creer-dpi' , creer_dpi),
      path('/ajouter-soin' , ajouter_soin),
      path('/ajouter-bilan-radiologique' , ajouter_Bilan_radiologique)
]