from rest_framework import serializers

from utilisateur.serializer import PatientSerializer

from .models import Consultation, ContactUrgence, Dpi, Examen, Medicament, Outil, Soin


# contact_urgence Serializer
class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgence
        fields = ("id", "nom", "prenom", "telephone", "email")


class DpiSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    contact_urgence = ContactUrgenceSerializer()

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
        fields = ("id", "date", "observation", "coup", "dpi_id", "dpi")
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
    consultation_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Examen
        fields = ("id", "type", "note", "traite", "consultation_id")
        extra_kwargs = {
            "type": {"required": True},
        }


# Outil Serializer
class OutilSerializer(serializers.ModelSerializer):
    class Meta:
        model: Outil
        fields = ("id", "nom")
        extra_kwargs = {"nom": {"required": True}}
