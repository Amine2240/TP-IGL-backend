from django.urls import path
from .views import *

urlpatterns = [
      path('/creer_consultation' , creer_consultation)
]