import cloudinary.uploader
from decouple import config
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from utilisateur.models import Medecin, Patient, Utilisateur
from utilisateur.serializer import MedecinSerializer

# Create your views here.


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_email = request.data.get("username")
        password = request.data.get("password")

        if not username_email or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = (
            Utilisateur.objects.filter(username=username_email).first()
            or Utilisateur.objects.filter(email=username_email).first()
        )
        if not user or not user.check_password(password):
            raise AuthenticationFailed("Incorrect username or password")

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response(
            {
                "message": "Login successful",
            }
        )

        response.set_cookie(
            key="auth_token",
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
        )
        return response


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nom": user.nom,
            "prenom": user.prenom,
            "role": user.role,
            "photoProfil": user.photo_profil,
            "telephone": user.telephone,
            "adresse": user.adresse,
            "dateDeNaissance": user.date_naissance,
        }

        return Response(user_data, status=status.HTTP_200_OK)


class ListPatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all()

        patient_data = []
        for patient in patients:
            patient_data.append(
                {
                    "patientId": patient.id,
                    "nom": patient.user.nom,
                    "prenom": patient.user.prenom,
                    "email": patient.user.email,
                    "photoProfil": patient.user.photo_profil,
                    "telephone": patient.user.telephone,
                    "dateDeNaissance": patient.user.date_naissance,
                    "adresse": patient.user.adresse,
                    "NSS": patient.NSS,
                    "dpiId": patient.dossier_patient.id,
                    "qrCode": patient.dossier_patient.qr_code,
                }
            )
        return Response(patient_data, status=status.HTTP_200_OK)


# Listing our brave doctors
class MedecinListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer


class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if "profilePicture" not in request.FILES:
            return Response(
                {"error": "No file provided. Please upload a profile picture."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile_picture = request.FILES["profilePicture"]

        try:
            # Uploading the image to the cloud
            upload_result = cloudinary.uploader.upload(
                profile_picture,
                folder="profile_pictures",
                public_id=f"user_{user.id}",
                overwrite=True,
                resource_type="image",
            )

            # getting teh url which's gonna be saved into db
            profile_picture_url = upload_result.get("url")

            # Saving to db
            user.photo_profil = profile_picture_url
            user.save()

            return Response(
                {
                    "message": "Profile picture updated successfully.",
                    "profile_picture_url": profile_picture_url,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while uploading the image: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
