from rest_framework import serializers 
from .models import Dpi , Consultation  , Hopital
from utilisateur.models import Medecin

#serializer pour l'Hopital
class HopitalSerializer(serializers.ModelSerializer):
    class Meta :
        model = Hopital 
        fields = ('id' , 'nom' , 'lieu' , 'data_debut_service')


#serializer pour la Consultation
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation 
        fields = (
            'id' , 'date_de_consultation' ,'note', 'dpi_id' , 'dpi' , 'medcin_id', 'medcin' , 'hopital_id' , 'hopital' 
            )
        extre_kwargs ={
            'note': {'required':False},
            'date_de_consultation' : {'read_only':True},
            'medcin' :{'read_only':True},
            'hopital' : {'read_only':True},
            'dpi' : {'read_only':True}
        }
    # redefinition de la methode create pour creer une consultation
    def create(self ,validated_data):
        # extraire les donnees necessaires a la creation de la consultation
        dpi_id = validated_data.pop('dpi_id' , None)
        medcin_id = validated_data.pop('medcin_id' , None)
        hopital_id = validated_data.pop('hopital_id' , None)
        # verifier si les donnees necessaires sont presentes
        if not dpi_id:
            raise serializers.ValidationError("Le DPI est obligatoire")
        if not medcin_id:
            raise serializers.ValidationError("Le medcin est obligatoire")
        if not hopital_id:
            raise serializers.ValidationError("L'hopital est obligatoire")
        
        # verifier si le DPI , le medcin et l'hopital existent
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except Dpi.DoesNotExist:
            raise serializers.ValidationError("Le DPI n'existe pas")
        try:
            medcin = Medecin.objects.get(id=medcin_id)
        except Medecin.DoesNotExist:
            raise serializers.ValidationError("Le medcin n'existe pas")
        try:
            hopital = Hopital.objects.get(id=hopital_id)
        except Hopital.DoesNotExist:
            raise serializers.ValidationError("L'hopital n'existe pas")
        validated_data['dpi'] = dpi
        validated_data['medcin'] = medcin
        validated_data['hopital'] = hopital
        return super().create(validated_data)