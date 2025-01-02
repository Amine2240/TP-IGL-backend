from django.urls import path

from dpi.views import PatientBilanBiologiqueView

from .views import (
    ListPatientsView,
    Login,
    MedecinListView,
    UpdatePatientProfilePictureView,
    UpdateProfilePictureView,
    UserInfoView,
)

urlpatterns = [
    path("login/", Login.as_view()),
    path("user-info/", UserInfoView.as_view()),
    path("patients/", ListPatientsView.as_view(), name="patients-list"),
    path(
        "patients/<int:patient_id>/update-profile-picture/",
        UpdatePatientProfilePictureView.as_view(),
        name="update_patient_profile_picture",
    ),

    path(
        "patients/<int:patient_id>/bilans/biologique/",
        PatientBilanBiologiqueView.as_view(),
        name="patient_bilans_biologique",
    ),
    path("medecins/", MedecinListView.as_view(), name="medecins-list"),
    path(
        "update-profile-picture/",
        UpdateProfilePictureView.as_view(),
        name="update-profilepicture",
    ),
]
