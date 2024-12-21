from rest_framework import serializers
from .models import Dpi , Consultation ,Hopital , ContactUrgence , Soin , Medicament ,  Examen  ,Outil  , DpiSoin , BilanRadiologique ,Mutuelle
from utilisateur.serializer import PatientSerializer , RadiologueSerializer
from utilisateur.models import Radiologue
import cloudinary.uploader



# contact_urgence Serializer
class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgence
        fields = (
            "id",
            "nom", 
            "prenom", 
            "telephone", 
            "email"
            )

#hopital Serializer
class HopitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hopital 
        fields= (
            "id" , 
            "nom",
            "lieu",
            "date_debut_service"
        ) 

class DpiSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    contact_urgence = ContactUrgenceSerializer()
    hopital_initial = HopitalSerializer(read_only=True)
    mutuelle= serializers.CharField(write_only=True)
    hopital_initial_id = serializers.CharField(write_only=True)

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
        )
        extra_kwargs = {
            "qr_code": {"read_only": True},
        }

    def create(self, validated_data):

        # Extract patient and contact_urgence data
        patient_data = validated_data.pop("patient", None)
        contact_urgence_data = validated_data.pop("contact_urgence", None)
        hopital_initial_id = validated_data.pop("L'hopital est obligatoire" ,None)

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
        if not hopital_initial_id :
             raise serializers.ValidationError(
                "L'hopital est obligatoire"
            )

        # Create or get the Patient object
        patient = PatientSerializer.create(
            PatientSerializer(), validated_data=patient_data
        )
        mutuelle_nom = validated_data.pop("mutuelle" , None)
        if not mutuelle_nom:
            raise serializers.ValidationError("Le nom de mutuelle est obligatoire .")
        
        Mutuelle.objects.create(nom = mutuelle_nom , patient= patient)
        # Handle ContactUrgence
        telephone = contact_urgence_data.get("telephone")
        try:
            # Try to get the existing contact_urgence by telephone
            contact_urgence = ContactUrgence.objects.get(telephone=telephone)

        except ContactUrgence.DoesNotExist:
            # Create a new contact_urgence if it doesn't exist
            contact_urgence = ContactUrgence.objects.create(**contact_urgence_data)
        if contact_urgence.nom != contact_urgence_data.get('nom') or contact_urgence.prenom != contact_urgence_data.get('prenom') or contact_urgence.email != contact_urgence_data.get('email'):
            raise serializers.ValidationError("Le contact d'urgence existe déjà avec un autre numéro de téléphone")
        #hopital 
        try:
            hopital_initial = Hopital.objects.get(id=hopital_initial_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError("L'hopital que vous avez mentione n'existe pas")
        # Attach the objects to validated_data
        validated_data["patient"] = patient
        validated_data["contact_urgence"] = contact_urgence
        validated_data["hopital_initial"] = hopital_initial 
       

        # Create the DPI object
        dpi = super().create(validated_data=validated_data)

        # Generate the QR code after creation
        dpi.generate_qr_code()

        return dpi


# serializer pour le soin
class SoinSerializer(serializers.ModelSerializer):
     class Meta :
        model = Soin 
        fields = ('id' ,'type')

     


#serializer pour le soin
class DpiSoinSerializer(serializers.ModelSerializer):
    dpi = DpiSerializer(read_only=True) 
    dpi_id = serializers.IntegerField(write_only=True)
    type = serializers.CharField(write_only=True) 
    class Meta :
        model = DpiSoin 
        fields = (
            'id' ,
            'date' ,
            'observation' ,
            'type',
            'dpi_id',
            'dpi'
            )
        extra_kwargs = {
            'dpi' : {'read_only':True},
            'date': {'read_only':True}
             
            }
    # redefinition de la methode create pour creer un soin 
    def create(self, validated_data):
        # extraire les donnees necessaires a la creation du soin
        dpi_id = validated_data.pop('dpi_id' , None)
        type = validated_data.pop('type' , None)

        # verifier si le DPI existe
        if not type:
            raise serializers.ValidationError("Le type du soin est obligatoire")
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")
        try :
            soin = Soin.objects.get( type = type) 
        except Soin.DoesNotExist:
             soin = Soin.objects.create(type=type)
        validated_data['soin'] = soin
        validated_data['dpi'] = dpi
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
   
    class Meta:
        model = Examen
        fields = (
            "id", 
            "type", 
            "note",
            "resultats",
            "traite"
            )
        extra_kwargs = {
            "type": {"required": True},
        }
    def update(self, instance, validated_data):
        resultats = validated_data.pop('resultats', None)
        if not resultats:
            raise serializers.ValidationError("Les resultats de l'examen sont obligatoires")
        # Mettre a jour les resultats de l'examen
        instance.resultats = resultats 
        # Mettre a jour le champ traite
        instance.traite = True 
        instance.save()
        return instance



# Outil Serializer
class OutilSerializer(serializers.ModelSerializer):
    class Meta:
        model:Outil 
        fields =('id' , 'nom')
        extra_kwargs={
            'nom' : {'required':True}
        }


#BilanRadiologique Serializer
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    radiologue = RadiologueSerializer(read_only=True)
    radiologue_id = serializers.IntegerField(write_only=True)
    examen = ExamenSerializer()
    # recevoir les images radiologiques
    images_radio = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    class Meta:
        model= BilanRadiologique 
        fields = (
            'id' , 
            'images_radio', 
            'examen',
            'radiologue' ,
            'radiologue_id'
            )

    def create(self, validated_data):
        # extraire les donnees necessaires a la creation du bilan radiologique
        radiologue_id = validated_data.pop('radiologue_id' , None)
        if not radiologue_id:
            raise serializers.ValidationError("Le radiologue est obligatoire")
        try:
            radiologue = Radiologue.objects.get(id=radiologue_id)
        except Radiologue.DoesNotExist:
            raise serializers.ValidationError("Le radiologue n'existe pas")
        validated_data['radiologue'] = radiologue
        print("validate data :")
        print(validated_data['examen'])
        # extraire les images radiologiques 
        image_files = validated_data.pop('images_radio', [])
        urls = []
        for image in image_files:
            # Téléchargement vers Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(image)
                urls.append(upload_result['url'])
            except Exception as e:
                raise serializers.ValidationError("Erreur lors de l'ajout de l'image radiologique")
        # Associer les URLs au champ images_radio
        validated_data['images_radio'] = urls
        return super().create(validated_data)
    
