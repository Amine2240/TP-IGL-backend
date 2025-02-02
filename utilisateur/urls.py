from django.urls import path

from dpi.views import (
    PatientBilanBiologiqueView,
    patient_antecedants,
    patient_bilan_radiogique,
)

from .views import (
    ListPatientsView,
    Login,
    Logout,
    MedecinListView,
    UpdatePatientProfilePictureView,
    UpdateProfilePictureView,
    UserInfoView,
)

urlpatterns = [
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
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
    path(
        "patients/<int:patient_id>/bilans/radiologique/",
        patient_bilan_radiogique,
        name="patient_bilans_radiologique",
    ),
    path(
        "patients/<int:patient_id>/antecedants/",
        patient_antecedants,
    ),
    path("medecins/", MedecinListView.as_view(), name="medecins-list"),
    path(
        "update-profile-picture/",
        UpdateProfilePictureView.as_view(),
        name="update-profilepicture",
    ),
]
