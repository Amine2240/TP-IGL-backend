from rest_framework import serializers 
from .models import Dpi , Consultation  , Hopital
from utilisateur.models import Medecin
from utilisateur.serializer import MedecinSerializer
from utilisateur.serializer import PatientSerializer

#serializer pour le DPI
class DpiSerializer(serializers.ModelSerializer):
    
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = Dpi
        fields = ('id' ,'patient' , 'hopital_initial' ,'qr_code',)
        extra_kwargs={
            'qr_code' :{'read_only':True},
            'patient' :{'read_only':True}
        }
    

#serializer pour l'Hopital
class HopitalSerializer(serializers.ModelSerializer):
    class Meta :
        model = Hopital 
        fields = ('id' , 'nom' , 'lieu' , 'date_debut_service')


#serializer pour la Consultation
class ConsultationSerializer(serializers.ModelSerializer):
    # champs necessaires a la creation de la consultation
    medecin = MedecinSerializer(read_only=True)
    hopital = HopitalSerializer(read_only=True)
    hopital_id = serializers.IntegerField(write_only=True)
    dpi_id = serializers.IntegerField(write_only=True)
    medecin_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Consultation 
        fields = (
            'id' , 'date_de_consultation' ,'notes', 'dpi_id'  , 'medecin_id' , 'medecin', 'hopital_id' , 'hopital' 
            )
        extre_kwargs ={
            'medecin' :{'read_only':True},
            'hopital' : {'read_only':True},
            'dpi' : {'read_only':True},
            'date_de_consultation' : {'read_only':True},
        }
    # redefinition de la methode create pour creer une consultation
    def create(self ,validated_data):
        # extraire les donnees necessaires a la creation de la consultation
        dpi_id = validated_data.pop('dpi_id' , None)
        medecin_id = validated_data.pop('medecin_id' , None)
        hopital_id = validated_data.pop('hopital_id' , None)
        # verifier si les donnees necessaires sont presentes
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        if not medecin_id:
            raise serializers.ValidationError("Le medcin est obligatoire")
        if not hopital_id:
            raise serializers.ValidationError("L'hopital est obligatoire")
        
        # verifier si le DPI , le medcin et l'hopital existent
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            raise serializers.ValidationError("Le medcin n'existe pas")
        try:
            hopital = Hopital.objects.get(id=hopital_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError("L'hopital n'existe pas")
        validated_data['dpi'] = dpi
        validated_data['medecin_principal'] = medecin
        validated_data['hopital'] = hopital
        return super().create(validated_data)