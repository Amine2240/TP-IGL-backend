from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dpi.models import BilanBiologique, Dpi, Examen
from utilisateur.models import Laborantin, Medecin, Patient

from .serializer import (
    ConsultationSerializer,
    DpiSerializer,
    ExamenSerializer,
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
        # getting params
        traite_param = request.query_params.get("traite")
        type_param = request.query_params.get("type")

        if traite_param is not None:
            if traite_param.lower() == "true":
                traite = True
            elif traite_param.lower() == "false":
                traite = False
            else:
                return Response(
                    {"error": "'traite' must be 'true' or 'false'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            traite = None

        allowed_types = ["radiologique", "biologique"]
        if type_param is not None:
            if type_param.lower() not in allowed_types:
                return Response(
                    {"error": "Exam type can be either 'radiologique' or 'biologique'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Exam type should be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Filtering queryset based on params
        exams = Examen.objects.all()
        if traite is not None:
            exams = exams.filter(traite=traite)
        if type_param:
            exams = exams.filter(type=type_param.lower())

        # Customizing the output data --> this can be changed base on the frontend need
        # just gimme a call !
        data = []
        for exam in exams:
            data.append(
                {
                    "id": exam.id,
                    "type": exam.type,
                    "traite": exam.traite,
                    "note": exam.note,
                    "resultats": exam.resultats,
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


class CreateBilanBiologiqueView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        examen_id = request.data.get("examen_id")

        user = request.user
        if not Laborantin.objects.filter(user=user).exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        laborantin_id = request.user.laborantin.id
        examen = get_object_or_404(Examen, id=examen_id)

        # validating exams types
        if examen.type != "biologique":
            return Response(
                {"error": "This exam is not 'biologique'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if examen.traite:
            return Response(
                {"error": "This exam has already been treated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Checcking if the a bilan has already been created for this exam
        if hasattr(examen, "bilanbiologique"):
            return Response(
                {"error": "A Bilan Biologique already exists for this exam."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bilan_biologique = BilanBiologique.objects.create(
            laborantin_id=laborantin_id, examen=examen
        )
        return Response(
            {
                "message": "Bilan Biologique successfully created.",
                "bilan_biologique_id": bilan_biologique.id,
                "laborantin_id": laborantin_id,
                "examen_id": examen_id,
            },
            status=status.HTTP_201_CREATED,
        )


class DpiDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            dpi = Dpi.objects.get(patient=patient)
        except Dpi.DoesNotExist:
            return Response(
                {"error": "Dossier Patient (Dpi) not found for this patient"},
                status=status.HTTP_404_NOT_FOUND,
            )

        contact_urgence = dpi.contact_urgence
        mutuelle = patient.mutuelles.all()[0].nom

        dpi_data = {
            "dpiId": dpi.id,
            "dateCreation": dpi.date_creation,
            "nom": patient.user.nom,
            "prenom": patient.user.prenom,
            "dateDeNaissance": patient.user.date_naissance,
            "adresse": patient.user.adresse,
            "NSS": patient.NSS,
            "telephone": patient.user.telephone,
            "mutuelle": mutuelle,
            "contact_urgence": {
                "nom": contact_urgence.nom,
                "prenom": contact_urgence.prenom,
                "telephone": contact_urgence.telephone,
                "email": contact_urgence.email,
            },
        }
        return Response(
            dpi_data,
            status=status.HTTP_200_OK,
        )
