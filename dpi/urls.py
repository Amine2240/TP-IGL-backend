from django.urls import path

from .views import *

# les urls de l'application dpi
urlpatterns = [
    path("creer-dpi", creer_dpi, name="creer-dpi"),
    path("ajouter-soin", ajouter_soin, name="ajouter-soin"),
    path("<int:patient_id>/", DpiDetailView.as_view(), name="non-treated-exams"),
    path("outils/", OutilListView.as_view(), name="outils"),
    path("soins/", SoinListView.as_view(), name="soins"),
    path("consultations/create/", ConsultationCreateView.as_view()),
    path("consultations/", ConsultationListView.as_view(), name="consultation-list"),
    path(
        "consultations/<int:patient_id>/",
        ConsultationListView.as_view(),
        name="consultation-list-patient",
    ),
    path("examens/", ExamenListView.as_view(), name="non-treated-exams"),
    path("bilans/biologique/", CreateBilanBiologiqueView.as_view()),
    path(
        "bilans/biologique/<int:bilan_id>/graph-values/",
        GraphValuesView.as_view(),
        name="graph_values",
    ),
    path("bilans/radiologique/<int:pk_examen>/", ajouter_Bilan_radiologique),
    path("creer-hospitalisation/<int:pk_patient>/", creer_hospitalisation),
]
