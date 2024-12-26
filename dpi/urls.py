from django.urls import path

from .views import *

# les urls de l'application dpi
urlpatterns = [
    path("/creer-dpi", creer_dpi),
    path("/ajouter-soin", ajouter_soin),
    path("ajouter-bilan-radiologique/", ajouter_Bilan_radiologique),
    path("<int:patient_id>/", DpiDetailView.as_view(), name="non-treated-exams"),
    path("examens/", ExamenListView.as_view(), name="non-treated-exams"),
    path("consultations/", ConsultationCreateView.as_view()),
    path("examens/", ExamenListView.as_view(), name="non-treated-exams"),
    path("bilans/biologique/", CreateBilanBiologiqueView.as_view()),
]
