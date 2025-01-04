from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from dpi.models import (
    BilanBiologique,
    BilanRadiologique,
    Consultation,
    Dpi,
    Examen,
    Outil,
    Parametre,
    ParametreValeur,
    Soin,
)
from utilisateur.models import (
    Utilisateur,
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Patient,
    Radiologue,
)

from .serializer import (
    Antecedant,
    BilanRadiologiqueSerializer,
    ConsultationReadSerializer,
    ConsultationSerializer,
    DpiSerializer,
    DpiSoinSerializer,
    ExamenSerializer,
    HospitalisationSerializer,
    OutilSerializer,
    SoinSerializer,
)
from .utils import decode_token, maj_examen, upload_image_to_cloudinary


@api_view(["POST"])  # decorateur pour la methode creer_patient
@permission_classes([IsAuthenticated])
def creer_dpi(request):
    user = request.user
    print("dpi _creations")
    print(request.data.get("patient").get("user").get("telephone"))
    if request.method == "POST":
        if not Administratif.objects.filter(user=user).exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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


# ajouter soin
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ajouter_soin(request):

    user = request.user

    if not Infermier.objects.filter(user=user).exists():
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = {}
    data = request.data.copy()
    data["infermier_id"] = Infermier.objects.get(user=user).id
    print(data)
    dpi_soin_serializer = DpiSoinSerializer(data=data)
    if dpi_soin_serializer.is_valid():
        dpi_soin_serializer.save()
        return Response(
            {
                "message": "Le soin a été ajouté avec succès",
            },
            status=status.HTTP_201_CREATED,
        )
    print(dpi_soin_serializer.errors)
    return Response(dpi_soin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ajouter bilan radiologique
@api_view(["POST"])
def ajouter_Bilan_radiologique(request, pk_examen):
    user_id=request.data.get('userId')
    print(user_id)
    resultats = request.data.get('examen[resultats]')
    print(resultats)
    user = Utilisateur.objects.filter(id=user_id).first()
    
    if not Radiologue.objects.filter(user=user).exists():
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    examen = get_object_or_404(Examen, id=pk_examen)
    if examen.type != "radiologique":
        return Response(
            {"error": "This exam is not 'radiologique'."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if examen.traite:
        return Response(
            {"error": "This exam has already been treated."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    print(pk_examen)
    try:
        examen = maj_examen(pk_examen, resultats=resultats)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Examen.DoesNotExist:
        return Response(
            {"error": "Examen n'existe pas."}, status=status.HTTP_404_NOT_FOUND
        )
    data = {
        "examen_id": pk_examen,
        "radiologue_id": Radiologue.objects.get(user_id=user_id).id,
        "images_radio": request.FILES.getlist("images_radio"),
    }
    print("data ", data)

    serializer_bilan_radiologique = BilanRadiologiqueSerializer(
        data=data,
    )
    if serializer_bilan_radiologique.is_valid():
        bilan = serializer_bilan_radiologique.save()
        return Response(
            {"Message": "Le bilan a été ajouté avec succès"},
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer_bilan_radiologique.errors, status=status.HTTP_400_BAD_REQUEST
    )


# creer hospitalisation
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def creer_hospitalisation(request, pk_patient):

    user = request.user
    user_id = user.id
    if not Administratif.objects.filter(user=user).exists():
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = {}
    data = request.data.copy()
    data.update(
        {
            "patient_id": pk_patient,
            "creer_par_id": Administratif.objects.get(user_id=user_id).id,
        }
    )
    hospitalisation_serializer = HospitalisationSerializer(data=data)
    if hospitalisation_serializer.is_valid():
        hospitalisation_serializer.save()
        return Response(
            {
                "message": "L'hospitalisation a été créée avec succès",
                "hospitalisation": hospitalisation_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        hospitalisation_serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


# get bilan radiologique
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def patient_bilan_radiogique(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    dpi = Dpi.objects.get(patient=patient)
    examens = Examen.objects.filter(consultation__dpi=dpi)

    bilan_radiologique = BilanRadiologique.objects.filter(examen__in=examens)

    if not bilan_radiologique.exists():
        return Response(
            {
                "message": f"No Bilan Radiologique records found for patient with ID {patient_id}."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    data = [
        {
            "id": bilan.id,
            "radiologue": bilan.radiologue.user.username,
            "images_radio": bilan.images_radio,
            "examen_id": bilan.examen.id,
            "examen_note": bilan.examen.note,
            "examen_type": bilan.examen.type,
            "examen_status": bilan.examen.traite,
            "examen_resultats": bilan.examen.resultats,
        }
        for bilan in bilan_radiologique
    ]

    return Response(data, status=200)


# get antecendants
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def patient_antecedants(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    dpi = Dpi.objects.get(patient=patient)
    antecedants = Antecedant.objects.filter(dpi=dpi)
    print(antecedants)
    data = [
        {
            "id": antecedant.id,
            "nom": antecedant.nom,
            "type": antecedant.type,
        }
        for antecedant in antecedants
    ]
    print(data)
    return Response(data, status=status.HTTP_200_OK)


# get bilan radiologique
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def patient_bilan_radiogique(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    dpi = Dpi.objects.get(patient=patient)
    examens = Examen.objects.filter(consultation__dpi=dpi)

    bilan_radiologique = BilanRadiologique.objects.filter(examen__in=examens)

    if not bilan_radiologique.exists():
        return Response(
            {
                "message": f"No Bilan Radiologique records found for patient with ID {patient_id}."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    data = [
        {
            "id": bilan.id,
            "radiologue": bilan.radiologue.user.username,
            "images_radio": bilan.images_radio,
            "examen_id": bilan.examen.id,
            "examen_note": bilan.examen.note,
            "examen_type": bilan.examen.type,
            "examen_status": bilan.examen.traite,
            "examen_resultats": bilan.examen.resultats,
        }
        for bilan in bilan_radiologique
    ]

    return Response(data, status=200)


# get antecendants
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def patient_antecedants(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    dpi = Dpi.objects.get(patient=patient)
    antecedants = Antecedant.objects.filter(dpi=dpi)
    print(antecedants)
    data = [
        {
            "id": antecedant.id,
            "nom": antecedant.nom,
            "type": antecedant.type,
        }
        for antecedant in antecedants
    ]
    print(data)
    return Response(data, status=status.HTTP_200_OK)


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


class ConsultationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id=None):
        if patient_id:
            consultations = Consultation.objects.filter(dpi__patient__id=patient_id)
        else:
            consultations = Consultation.objects.all()

        serializer = ConsultationReadSerializer(consultations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ExamenListViewPatient(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        traite_param = request.query_params.get("traite")
        type_param = request.query_params.get("type")
        patient_id = request.query_params.get("patient_id")

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

        if patient_id is not None:
            try:
                patient_id = int(patient_id)
            except ValueError:
                return Response(
                    {"error": "'patient_id' must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        exams = Examen.objects.all()

        if traite is not None:
            exams = exams.filter(traite=traite)

        if type_param:
            exams = exams.filter(type=type_param.lower())

        if patient_id:
            exams = exams.filter(consultation__dpi__patient__id=patient_id)

        # Customizing the output data --> this can be changed based on the frontend need
        # just gimme a call !
        data = []
        for exam in exams:
            data.append(
                {
                    "id": exam.id,
                    "type": exam.type,
                    "traite": exam.traite,
                    "date": exam.consultation.date_de_consultation,
                    "note": exam.note,
                    "resultats": exam.resultats,
                    "doctor": {
                        "id": exam.consultation.medecin_principal.id,
                        "nom": exam.consultation.medecin_principal.user.nom,
                        "prenom": exam.consultation.medecin_principal.user.prenom,
                        "specialite": exam.consultation.medecin_principal.specialite,
                    },
                }
            )

        return Response(data, status=status.HTTP_200_OK)


class CreateBilanBiologiqueView(APIView):
    

    def post(self, request):
        permission_classes = [IsAuthenticated]
        examen_id = request.data.get("examen_id")
        print(examen_id)
        graph_values = request.data.get("graph_values")
        resultats = request.data.get("resultats")
        user_id = request.data.get("user_id")
        missing_fields = []
        if not examen_id:
            missing_fields.append("examen_id")
        if not graph_values:
            missing_fields.append("graph_values")
        if not resultats:
            missing_fields.append("resultats")

        if missing_fields:
            return Response(
                {
                    "error": f"The following fields are required: {', '.join(missing_fields)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is a Laborantin
        user = Utilisateur.objects.filter(id=user_id).first()
      
        print(user.laborantin.id)
        if not Laborantin.objects.filter(user=user).exists():
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        laborantin_id = user.laborantin.id
        examen = get_object_or_404(Examen, id=examen_id)

        # Validate exam type
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

        # Check if a BilanBiologique already exists for this exam
        if hasattr(examen, "bilanbiologique"):
            return Response(
                {"error": "A Bilan Biologique already exists for this exam."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the BilanBiologique
        bilan_biologique = BilanBiologique.objects.create(
            laborantin_id=user_id, examen=examen
        )

        if graph_values:
            for param in graph_values:
                parametre_name = param.get("parametre")
                valeur = param.get("valeur")

                if not parametre_name or not valeur:
                    return Response(
                        {
                            "error": "Each parameter must have a 'parametre' name and 'valeur'."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                parametre, _ = Parametre.objects.get_or_create(nom=parametre_name)

                ParametreValeur.objects.create(
                    parametre=parametre,
                    bilan_biologique=bilan_biologique,
                    valeur=valeur,
                )

        examen.resultats = resultats
        examen.traite = True
        examen.save()
        return Response(
            {
                "message": "Bilan Biologique successfully created.",
                "bilan_biologique_id": bilan_biologique.id,
                "laborantin_id": user_id,
                "examen_id": examen_id,
            },
            status=status.HTTP_201_CREATED,
        )


class PatientBilanBiologiqueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
      
        patient = get_object_or_404(Patient, id=patient_id)
        dpi = Dpi.objects.get(patient=patient)
        examens = Examen.objects.filter(consultation__dpi=dpi)

        bilan_biologiques = BilanBiologique.objects.filter(examen__in=examens)

        if not bilan_biologiques.exists():
            return Response(
                {
                    "message": f"No Bilan Biologique records found for patient with ID {patient_id}."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        data = [
            {
                "id": bilan.id,
                "laborantin": bilan.laborantin.user.username,
                "examen_id": bilan.examen.id,
                "examen_note": bilan.examen.note,
                "examen_type": bilan.examen.type,
                "examen_status": bilan.examen.traite,
                "examen_resultats": bilan.examen.resultats,
            }
            for bilan in bilan_biologiques
        ]

        return Response(data, status=200)


class GraphValuesView(APIView):
    

    def get(self, request, bilan_id):
        permission_classes = [IsAuthenticated]
        bilan = get_object_or_404(BilanBiologique, id=bilan_id)

        parametre_values = ParametreValeur.objects.filter(bilan_biologique=bilan)

        data = [
            {
                "parametre_id": parametre.parametre.id,
                "parametre_name": parametre.parametre.nom,
                "value": parametre.valeur,
            }
            for parametre in parametre_values
        ]

        return Response(data, status=200)


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


class OutilListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Outil.objects.all()
    serializer_class = OutilSerializer


class SoinListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Soin.objects.all()
    serializer_class = SoinSerializer