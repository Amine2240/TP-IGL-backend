from rest_framework import serializers 
from .models import Dpi , Consultation  , ContactUrgence , Soin , Medicament ,  Examen , Bilan ,Outil  , DpiSoin , BilanRadiologique
from utilisateur.serializer import PatientSerializer , RadiologueSerializer
from utilisateur.models import Radiologue


#contact_urgence Serializer
class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgence
        fields = ('id' , 'nom' , 'prenom' , 'telephone' , 'email')

    

class DpiSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    contact_urgence = ContactUrgenceSerializer()  

    class Meta:
        model = Dpi
        fields = ('id', 'patient', 'contact_urgence', 'hopital_initial', 'qr_code',)
        extra_kwargs = {
            'qr_code': {'read_only': True},
        }

    def create(self, validated_data):
        # Extract patient and contact_urgence data
        patient_data = validated_data.pop('patient', None)
        contact_urgence_data = validated_data.pop('contact_urgence', None)

        # Validate patient data
        if not patient_data:
            raise serializers.ValidationError("Les informations du patient sont obligatoires")

        # Validate contact_urgence data
        if not contact_urgence_data:
            raise serializers.ValidationError("Les informations de contact d'urgence sont obligatoires")

        # Create or get the Patient object
        patient = PatientSerializer.create(PatientSerializer(), validated_data=patient_data)

        # Handle ContactUrgence
        telephone = contact_urgence_data.get('telephone')
        try:
            # Try to get the existing contact_urgence by telephone
            contact_urgence = ContactUrgence.objects.get(telephone=telephone)
        
        except ContactUrgence.DoesNotExist:
            # Create a new contact_urgence if it doesn't exist
            contact_urgence = ContactUrgence.objects.create(**contact_urgence_data)
        if contact_urgence.nom != contact_urgence_data.get('nom') or contact_urgence.prenom != contact_urgence_data.get('prenom') or contact_urgence.email != contact_urgence_data.get('email'):
            raise serializers.ValidationError("Le contact d'urgence existe déjà avec un autre numéro de téléphone")
        # Attach the objects to validated_data
        validated_data['patient'] = patient
        validated_data['contact_urgence'] = contact_urgence

        # Create the DPI object
        dpi = super().create(validated_data=validated_data)

        # Generate the QR code after creation
        dpi.generate_qr_code()

        return dpi



    
#serializer pour le soin
class DpiSoinSerializer(serializers.ModelSerializer):
    dpi = DpiSerializer(read_only=True) 
    dpi_id = serializers.IntegerField(write_only=True)
    type = serializers.CharField(write_only=True) 
    class Meta :
        model = DpiSoin 
        fields = ('id' , 'date' , 'observation' ,'type', 'dpi_id','dpi')
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
    


#Medicament Serializer
class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament 
        fields = ('id' , 'nom' )
    
    def create(self, validated_data):
        nom = validated_data.pop('nom', None)
        if not nom:
            raise serializers.ValidationError("Le nom du medicament est obligatoire")
        try:
            medicament = Medicament.objects.get(nom=nom)
        except Medicament.DoesNotExist:
            validated_data['nom'] = nom
            medicament = super().create(validated_data)
        return medicament

#Examen Serializer
class ExamenSerializer(serializers.ModelSerializer):
    consultation_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Examen
        fields = ('id' , 'type' , 'note' , 'traite' ,'consultation_id')
        extra_kwargs = {
            'type' : {'required':True},
        }


        
        


#Bilan Serializer
class BilanSerializer(serializers.ModelSerializer):
    examen = ExamenSerializer(read_only=True)
    examen_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Bilan
        fields = ('id' , 'examen' , 'resultats' ,'examen_id')
        extra_kwargs = {
            'examen' : {'read_only':True},
            'resultat' : {'required':True}
            }


#Outil Serializer
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
    radioloque_id = serializers.IntegerField(write_only=True)
    bilan = BilanSerializer(read_only=True)
    
    class Meta:
        model: BilanRadiologique 
        fields = ('id' , 'bilan','radioloque' ,'radiologue_id')
        extra_kwargs = {
            'bilan' : {'read_only':True},
            'url' : {'required':True}
        }
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
        return super().create(validated_data)
    
