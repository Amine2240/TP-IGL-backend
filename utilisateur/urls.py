from django.urls import path
from .views import creer_patient

urlpatterns = [
    path('/creer_patient' , creer_patient)
]