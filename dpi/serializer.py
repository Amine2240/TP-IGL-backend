from rest_framework import serializers 
from .models import Dpi , Consultation  , ContactUrgence , Soin , Medicament ,  Examen , Bilan ,Outil 
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
    
#serializer pour le soin
class SoinSerializer(serializers.ModelSerializer):
    dpi = DpiSerializer(read_only=True) 
    dpi_id = serializers.IntegerField(write_only=True)
    class Meta :
        model = Soin 
        fields = ('id' , 'date' , 'observation' , 'coup' , 'dpi_id','dpi')
        extra_kwargs = {
            'dpi' : {'read_only':True},
            'date': {'read_only':True}
            }
    # redefinition de la methode create pour creer un soin 
    def create(self, validated_data):
        # extraire les donnees necessaires a la creation du soin
        dpi_id = validated_data.pop('dpi_id' , None)
        # verifier si le DPI existe
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")
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
    class Meta:
        model = Bilan
        fields = ('id' , 'examen' , 'resultats')
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




    
