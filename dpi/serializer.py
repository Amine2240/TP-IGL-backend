import cloudinary.uploader
from django.db.models.expressions import fields
from rest_framework import serializers

from utilisateur.models import (
    Administratif,
    Infermier,
    Medecin,
    Patient,
    Radiologue,
    Utilisateur,
)
from utilisateur.serializer import (
    AdministratifSerializer,
    InfermierSerializer,
    MedecinSerializer,
    PatientSerializer,
    RadiologueSerializer,
)

from .models import (
    Antecedant,
    BilanRadiologique,
    Consultation,
    ConsultationMedecin,
    ConsultationOutil,
    ContactUrgence,
    Dpi,
    DpiSoin,
    Examen,
    Hopital,
    Hospitalisation,
    Medicament,
    Mutuelle,
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


# hopital Serializer
class HopitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hopital
        fields = ("id", "nom", "lieu", "date_debut_service")


# serializer pour les antecedants
class AntecedantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antecedant
        fields = ("id", "nom", "type")


# dpi serializer
class DpiSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    contact_urgence = ContactUrgenceSerializer()
    hopital_initial = HopitalSerializer(read_only=True)
    mutuelle = serializers.CharField(write_only=True)
    hopital_initial_id = serializers.IntegerField(write_only=True)
    antecedants = AntecedantSerializer(many=True, write_only=True)
    qr_code = serializers.CharField(read_only=True)

    class Meta:
        model = Dpi
        fields = (
            "id",
            "patient",
            "contact_urgence",
            "hopital_initial_id",
            "hopital_initial",
            "mutuelle",
            "qr_code",
            "antecedants",
        )
        extra_kwargs = {
            "qr_code": {"read_only": True},
        }

    def create(self, validated_data):

        # Extract patient and contact_urgence data
        patient_data = validated_data.pop("patient", None)
        contact_urgence_data = validated_data.pop("contact_urgence", None)
        hopital_initial_id = validated_data.pop("hopital_initial_id", None)

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
        if not hopital_initial_id:
            raise serializers.ValidationError("L'hopital est obligatoire")
        antecedant_data = validated_data.pop("antecedants", None)
        print("validate data")
        print(validated_data)
        print(antecedant_data)
        # Create or get the Patient object
        patient = PatientSerializer.create(
            PatientSerializer(), validated_data=patient_data
        )
        mutuelle_nom = validated_data.pop("mutuelle", None)
        if not mutuelle_nom:
            raise serializers.ValidationError("Le nom de mutuelle est obligatoire .")

        Mutuelle.objects.create(nom=mutuelle_nom, patient=patient)
        # Handle ContactUrgence
        telephone = contact_urgence_data.get("telephone")
        try:
            # Try to get the existing contact_urgence by telephone
            contact_urgence = ContactUrgence.objects.get(telephone=telephone)

        except ContactUrgence.DoesNotExist:
            # Create a new contact_urgence if it doesn't exist
            contact_urgence = ContactUrgence.objects.create(**contact_urgence_data)
        if (
            contact_urgence.nom != contact_urgence_data.get("nom")
            or contact_urgence.prenom != contact_urgence_data.get("prenom")
            or contact_urgence.email != contact_urgence_data.get("email")
        ):
            raise serializers.ValidationError(
                "Le contact d'urgence existe déjà avec un autre numéro de téléphone"
            )
        # hopital
        try:
            hopital_initial = Hopital.objects.get(id=hopital_initial_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError(
                "L'hopital que vous avez mentione n'existe pas"
            )
        # Attach the objects to validated_data
        validated_data["patient"] = patient
        validated_data["contact_urgence"] = contact_urgence
        validated_data["hopital_initial"] = hopital_initial
        # Create the DPI object
        dpi = super().create(validated_data=validated_data)
        print(dpi)
        if antecedant_data:
            for antecedant in antecedant_data:
                Antecedant.objects.create(dpi=dpi, **antecedant)

        # Generate the QR code after creation
        dpi.generate_qr_code()

        return dpi


# serializer pour le soin
class SoinSerializer(serializers.ModelSerializer):
     observation = serializers.CharField(write_only=True)
     class Meta :
        model = Soin 
        fields = ('id' , 'observation' , 'nom' ,'type')

     
# serializer pour dpiSoin
class DpiSoinSerializer(serializers.ModelSerializer):
    soins = SoinSerializer(many=True)
    dpi = DpiSerializer(read_only=True)
    dpi_id = serializers.IntegerField(write_only=True)
    infermier_id = serializers.IntegerField(write_only=True)
    hopital = HopitalSerializer(read_only=True)
    hopital_id = serializers.IntegerField(write_only=True)
    infermier = InfermierSerializer(read_only=True)

    class Meta:
        model = DpiSoin
        fields = (
            'id',
            'date',
            'soins',
            'dpi_id',
            'dpi',
            'infermier',
            'infermier_id',
            'hopital_id',
            'hopital',
        )
        extra_kwargs = {
            'dpi': {'read_only': True},
            'date': {'read_only': True},
        }

    # Redéfinition de la méthode create pour gérer plusieurs soins
    def create(self, validated_data):
        soins_data = validated_data.pop('soins', None)  # Extraire la liste des soins
        dpi_id = validated_data.pop('dpi_id', None)
        infermier_id = validated_data.pop('infermier_id', None)
        hopital_id = validated_data.pop('hopital_id', None)

        # Validation et récupération des entités associées
        if not soins_data  :
            raise serializers.ValidationError("Les informations du soin sont obligatoires")
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")

        if not infermier_id:
            raise serializers.ValidationError("L'information de l'infirmier est obligatoire")
        try:
            infermier = Infermier.objects.get(id=infermier_id)
        except Infermier.DoesNotExist:
            raise serializers.ValidationError("L'infirmier n'existe pas")

        if not hopital_id:
            raise serializers.ValidationError("L'hôpital est obligatoire")
        try:
            hopital = Hopital.objects.get(id=hopital_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError("L'hôpital n'existe pas")

        # Créer les soins et les associer
        dpisoin_instances = []
        for soin_data in soins_data:
           
            nom = soin_data.get('nom')
            type = soin_data.get('type')
            observation = soin_data.get('observation')
            if not nom:
                raise serializers.ValidationError("Le nom du soin est obligatoire")
            if not type:
                raise serializers.ValidationError("Le type du soin est obligatoire")

            # Vérifier si le soin existe ou le créer
            soin, _ = Soin.objects.get_or_create(nom=nom, type=type)
        
            # Créer un DpiSoin pour ce soin spécifique
            dpisoin_instance = DpiSoin.objects.create(
                dpi=dpi,
                infermier=infermier,
                observation =observation ,
                hopital=hopital,
                soin=soin,
                **validated_data
            )
            print("dpi soins")
            print(dpisoin_instance)
            dpisoin_instances.append(dpisoin_instance)

        return dpisoin_instances


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

        def update(self, instance, validated_data):
            resultats = validated_data.pop("resultats", None)
            if not resultats:
                raise serializers.ValidationError(
                    "Les resultats de l'examen sont obligatoires"
                )
            # Mettre a jour les resultats de l'examen
            instance.resultats = resultats
            # Mettre a jour le champ traite
            instance.traite = True
            instance.save()
            return instance


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
    outils = serializers.PrimaryKeyRelatedField(queryset=Outil.objects.all(), many=True)
    medecins = serializers.PrimaryKeyRelatedField(
        queryset=Medecin.objects.all(), many=True
    )

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


# BilanRadiologique Serializer
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    radiologue = RadiologueSerializer(read_only=True)
    radiologue_id = serializers.IntegerField(write_only=True)
    examen = serializers.PrimaryKeyRelatedField(queryset=Examen.objects.all())
    # recevoir les images radiologiques
    images_radio = serializers.ListField(
        child=serializers.FileField()
    )
    class Meta:
        model = BilanRadiologique
        fields = ("id", "images_radio", "examen", "radiologue", "radiologue_id")

    def create(self, validated_data):
        # extraire les donnees necessaires a la creation du bilan radiologique
        radiologue_id = validated_data.pop("radiologue_id", None)
        if not radiologue_id:
            raise serializers.ValidationError("Le radiologue est obligatoire")
        try:
            radiologue = Radiologue.objects.get(id=radiologue_id)
        except Radiologue.DoesNotExist:
            raise serializers.ValidationError("Le radiologue n'existe pas")
        validated_data["radiologue"] = radiologue
        print("validate data :")
        # extraire les images radiologiques
        image_files = validated_data.pop("images_radio", [])
        urls = []
        for image in image_files:
            # Téléchargement vers Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(image)
                urls.append(upload_result["url"])
            except Exception as e:
                raise serializers.ValidationError(
                    "Erreur lors de l'ajout de l'image radiologique"
                )
        # Associer les URLs au champ images_radio
        validated_data["images_radio"] = urls
        return super().create(validated_data)


# Hospitalisation serializer
class HospitalisationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    hopital = HopitalSerializer(read_only=True)
    cree_par = AdministratifSerializer(read_only=True)
    creer_par_id = serializers.CharField(write_only=True)
    patient_id = serializers.CharField(write_only=True)
    hopital_id = serializers.CharField(write_only=True)
    date_sortie = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Hospitalisation
        fields = (
            "id",
            "date_entree",
            "date_sortie",
            "patient",
            "patient_id",
            "creer_par_id",
            "cree_par",
            "hopital_id",
            "hopital",
        )
        extra_kwargs = {
            "date_sortie": {"read_only": True},
        }

    def create(self, validated_data):
        # extraire les donnees necessaires a la creation de l'hospitalisation
        creer_par_id = validated_data.pop("creer_par_id", None)
        hopital_id = validated_data.pop("hopital_id", None)
        patient_id = validated_data.pop("patient_id", None)

        if not hopital_id:
            raise serializers.ValidationError("L'hopital est obligatoire")
        try:
            cree_par = Administratif.objects.get(id=creer_par_id)
        except Administratif.DoesNotExist:
            raise serializers.ValidationError("L'administratif n'existe pas")
        try:
            hopital = Hopital.objects.get(id=hopital_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError("L'hopital n'existe pas")
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Le patient n'existe pas")

        validated_data["cree_par"] = cree_par
        validated_data["hopital"] = hopital
        validated_data["patient"] = patient
        return super().create(validated_data)
