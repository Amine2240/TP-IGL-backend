from django.urls import path
from .views import * 

urlpatterns = [
    path('/creer_patient' , creer_patient)
]