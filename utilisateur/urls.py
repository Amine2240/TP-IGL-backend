from django.urls import path

from .views import (
    ListPatientsView,
    Login,
    MedecinListView,
    UpdateProfilePictureView,
    UserInfoView,
)

urlpatterns = [
    path("login/", Login.as_view()),
    path("user-info/", UserInfoView.as_view()),
    path("patients/", ListPatientsView.as_view(), name="patients-list"),
    path("medecins/", MedecinListView.as_view(), name="medecins-list"),
    path(
        "update-profile-picture/",
        UpdateProfilePictureView.as_view(),
        name="update-profilepicture",
    ),
]
