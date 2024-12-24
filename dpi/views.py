from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dpi.models import Examen
from utilisateur.models import Medecin

from .serializer import (
    ConsultationSerializer,
    DpiSerializer,
    ExamenSerializer,
    MedecinSerializer,
    SoinSerializer,
)
from .utils import upload_image_to_cloudinary


@api_view(["POST"])  # decorateur pour la methode creer_patient
def creer_dpi(request):
    if request.method == "POST":
        serializer = DpiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Le dossier patient a été créé avec succès",
                    "dpi": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# ajouter soin
def ajouter_soin(request):
    soin_serializer = SoinSerializer(data=request.data)
    if soin_serializer.is_valid():
        soin_serializer.save()
        return Response(
            {
                "message": "Le soin a été ajouté avec succès",
                "soin": soin_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(soin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# ajouter bilan radiologique
def ajouter_Bilan_radiologique(request):  # la fonction n'est pas encore complete
    try:
        url = upload_image_to_cloudinary(request)
        return Response(
            {"message": "L'image a été ajoutée avec succès", "url": url},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        print(e)
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConsultationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Checking in the user is a doctor --> onlly doctors can create consultation
        user = request.user
        if not Medecin.objects.filter(user=user).exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ConsultationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            consultation = serializer.save()
            print(consultation)
            return Response(
                {"detail": "Consultation created successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamenListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        non_treated_exams = Examen.objects.filter(traite=False)
        serializer = ExamenSerializer(non_treated_exams, many=True)
        if not serializer.is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Customizing the output data --> this can be changed base on the frontend need
        # just gimme a call !
        data = []
        for exam in non_treated_exams:
            data.append(
                {
                    "id": exam.id,
                    "type": exam.type,
                    "traite": exam.traite,
                    "note": exam.note,
                    "doctor": {
                        "id": exam.consultation.medecin_principal.id,
                        "nom": exam.consultation.medecin_principal.user.nom,
                        "prenom": exam.consultation.medecin_principal.user.prenom,
                        "specialite": exam.consultation.medecin_principal.specialite,
                    },
                    "patient": {
                        "id": exam.consultation.dpi.patient.id,
                        "nom": exam.consultation.dpi.patient.user.nom,
                        "prenom": exam.consultation.dpi.patient.user.prenom,
                    },
                }
            )
        return Response(data, status=status.HTTP_200_OK)


# Listing our brave doctors
class MedecinListView(generics.ListAPIView):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
