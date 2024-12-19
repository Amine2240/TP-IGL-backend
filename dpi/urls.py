from django.urls import path
from .views import *

#les urls de l'application dpi 
urlpatterns = [
      path('/ajouter-soin' , ajouter_soin),
      path('/ajouter-outil' , ajouter_outil),
      path('/ajouter-bilan-radiologique' , ajouter_Bilan_radiologique)
]