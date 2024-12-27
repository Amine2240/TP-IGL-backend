from django.db.models.expressions import fields
from rest_framework import serializers

from utilisateur.models import Medecin, Utilisateur
from utilisateur.serializer import MedecinSerializer, PatientSerializer

from .models import (
    Consultation,
    ConsultationMedecin,
    ConsultationOutil,
    ContactUrgence,
    Dpi,
    Examen,
    Hopital,
    Medicament,
    Ordonnance,
    Outil,
    Prescription,
    Resume,
    ResumeMesuresPrises,
    ResumeSymptomes,
    Soin,
)


# contact_urgence Serializer
class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgence
        fields = ("id", "nom", "prenom", "telephone", "email")


class HopitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hopital
        fields = ("id", "nom", "lieu")


class DpiSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    contact_urgence = ContactUrgenceSerializer()
    hopital_initial = HopitalSerializer()

    class Meta:
        model = Dpi
        fields = (
            "id",
            "patient",
            "contact_urgence",
            "hopital_initial",
            "qr_code",
        )
        extra_kwargs = {
            "qr_code": {"read_only": True},
        }

    def create(self, validated_data):
        # Extract patient and contact_urgence data
        patient_data = validated_data.pop("patient", None)
        contact_urgence_data = validated_data.pop("contact_urgence", None)

        # Validate patient data
        if not patient_data:
            raise serializers.ValidationError(
                "Les informations du patient sont obligatoires"
            )

        # Validate contact_urgence data
        if not contact_urgence_data:
            raise serializers.ValidationError(
                "Les informations de contact d'urgence sont obligatoires"
            )

        # Create or get the Patient object
        patient = PatientSerializer.create(
            PatientSerializer(), validated_data=patient_data
        )

        # Handle ContactUrgence
        telephone = contact_urgence_data.get("telephone")
        try:
            # Try to get the existing contact_urgence by telephone
            contact_urgence = ContactUrgence.objects.get(telephone=telephone)

        except ContactUrgence.DoesNotExist:
            # Create a new contact_urgence if it doesn't exist
            contact_urgence = ContactUrgence.objects.create(**contact_urgence_data)

        # Attach the objects to validated_data
        validated_data["patient"] = patient
        validated_data["contact_urgence"] = contact_urgence

        # Create the DPI object
        dpi = super().create(validated_data=validated_data)

        # Generate the QR code after creation
        dpi.generate_qr_code()

        return dpi


# serializer pour le soin
class SoinSerializer(serializers.ModelSerializer):
    dpi = DpiSerializer(read_only=True)
    dpi_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Soin
        fields = ("id", "nom", "observation", "type")
        extra_kwargs = {"dpi": {"read_only": True}, "date": {"read_only": True}}

    # redefinition de la methode create pour creer un soin
    def create(self, validated_data):
        # extraire les donnees necessaires a la creation du soin
        dpi_id = validated_data.pop("dpi_id", None)
        # verifier si le DPI existe
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")
        validated_data["dpi"] = dpi
        return super().create(validated_data)


# Medicament Serializer
class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = ("id", "nom")
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        nom = validated_data.pop("nom", None)
        if not nom:
            raise serializers.ValidationError("Le nom du medicament est obligatoire")
        try:
            medicament = Medicament.objects.get(nom=nom)
        except Medicament.DoesNotExist:
            validated_data["nom"] = nom
            medicament = super().create(validated_data)
        return medicament


# Examen Serializer
class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = ["id", "type", "note", "traite", "resultats"]
        extra_kwargs = {"id": {"read_only": True}}


class PrescriptionSerializer(serializers.ModelSerializer):
    medicament = MedicamentSerializer()

    class Meta:
        model = Prescription
        fields = ["id", "medicament", "dose", "duree", "heure", "nombre_de_prises"]
        extra_kwargs = {"id": {"read_only": True}}


class OrdonnanceSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True)

    class Meta:
        model = Ordonnance
        fields = ["id", "date_de_creation", "prescriptions"]
        extra_kwargs = {"id": {"read_only": True}}


class ConsultationMedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationMedecin
        fields = ["id", "consultation", "medecin"]


class ResumeSymptomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSymptomes
        fields = ["id", "symptome"]
        extra_kwargs = {"id": {"read_only": True}}


class ResumeMesurePriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeMesuresPrises
        fields = ["id", "mesure"]
        extra_kwargs = {"id": {"read_only": True}}


class ResumeSerializer(serializers.ModelSerializer):
    symptomes = ResumeSymptomeSerializer(many=True, write_only=True)
    mesures = ResumeMesurePriseSerializer(many=True, write_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "diagnostic",
            "date_prochaine_consultation",
            "symptomes",
            "mesures",
        ]
        extra_kwargs = {"id": {"read_only": True}}


# Outil Serializer
class OutilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outil
        fields = ("id", "nom")
        extra_kwargs = {"nom": {"required": True}}


class ConsultationSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceSerializer(many=True, write_only=True)
    examens = ExamenSerializer(many=True, write_only=True)
    resumes = ResumeSerializer(many=True, write_only=True)
    outils = OutilSerializer(many=True, write_only=True)

    class Meta:
        model = Consultation
        fields = [
            "id",
            "dpi",
            "hopital",
            "date_de_consultation",
            "heure",
            "ordonnances",
            "examens",
            "medecins",
            "resumes",
            "outils",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        ordonnances_data = validated_data.pop("ordonnances", [])
        examens_data = validated_data.pop("examens", [])
        medecins_data = validated_data.pop("medecins", [])
        resumes_data = validated_data.pop("resumes", [])
        outils_data = validated_data.pop("outils", [])

        request = self.context.get("request")
        user = request.user

        medecin_principal = Medecin.objects.get(user=user)

        consultation = Consultation.objects.create(
            medecin_principal=medecin_principal, **validated_data
        )
        # creating ordonnances
        for ordonnance_data in ordonnances_data:
            prescriptions_data = ordonnance_data.pop("prescriptions", [])
            ordonnance = Ordonnance.objects.create(
                consultation=consultation, **ordonnance_data
            )
            for prescription_data in prescriptions_data:
                medicament_data = prescription_data.pop("medicament")
                medicament, _ = Medicament.objects.get_or_create(**medicament_data)
                Prescription.objects.create(
                    ordonnance=ordonnance, medicament=medicament, **prescription_data
                )
        # creating resumes
        for resume_data in resumes_data:
            symptomes_data = resume_data.pop("symptomes", [])
            mesures_data = resume_data.pop("mesures", [])
            resume = Resume.objects.create(consultation=consultation, **resume_data)
            for symptome_data in symptomes_data:
                ResumeSymptomes.objects.create(resume=resume, **symptome_data)
            for mesure_data in mesures_data:
                ResumeMesuresPrises.objects.create(resume=resume, **mesure_data)

        # Create Examens and medecins_consultations as well as outils_consultation
        for examen_data in examens_data:
            Examen.objects.create(consultation=consultation, **examen_data)
        for medecin in medecins_data:
            ConsultationMedecin.objects.create(
                consultation=consultation, medecin=medecin
            )
        for outil in outils_data:
            ConsultationOutil.objects.create(consultation=consultation, outil=outil)
        return consultation


class ConsultationReadSerializer(serializers.ModelSerializer):
    ordonnances = OrdonnanceSerializer(many=True, read_only=True)
    examens = ExamenSerializer(many=True, read_only=True)
    outils = OutilSerializer(many=True, read_only=True)
    medecin_principal = MedecinSerializer(read_only=True)
    date_de_consultation = serializers.DateField(read_only=True)
    heure = serializers.TimeField(read_only=True)
    hopital = HopitalSerializer()

    class Meta:
        model = Consultation
        fields = [
            "id",
            "dpi",
            "hopital",
            "medecin_principal",
            "date_de_consultation",
            "heure",
            "ordonnances",
            "examens",
            "outils",
        ]
