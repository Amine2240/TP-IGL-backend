import random
import string
import bcrypt
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Utilisateur ,Patient  , Radiologue

Utilisateur = get_user_model()
#serializer pour l'utilisateur
class UtilisateurSerializer(serializers.ModelSerializer):#serializer pour l'utilisateur 
    class Meta:
        model = Utilisateur
        fields = ('id' ,'nom' ,'prenom' ,'date_naissance' ,'telephone' ,'photo_profil' ,'role' ,'email' ,'password')
        extra_kwargs ={
            'password' : {'write_only':True , 'required':False} 
            
        }
    # pour generer un mot de passe aleatoire et le crypter
    def generer_mot_de_passe():
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def create(self , validated_data):# redefinition de la methode create pour creer un utilisateur 

        role = validated_data.pop('role',None)

        if not role : 
            raise serializers.ValidationError("Le role est obligatoire")
        email = validated_data.pop('email',None)

        if not email:
            raise serializers.ValidationError("L'email est obligatoire")
        validated_data['username'] = email
        
        password = UtilisateurSerializer.generer_mot_de_passe()

        user = Utilisateur.objects.create_user(
            **validated_data ,role=role ,password = password , email = email
        )# creation de l'utilisateur
        return user  





#serializer pour le patient
class PatientSerializer(serializers.ModelSerializer):#serializer pour le patient
    user = UtilisateurSerializer()
    class Meta:
        model = Patient
        fields = ('id' , 'NSS' , 'user'  )
        extra_kwargs ={
            'NSS' : {'required':True} ,   
        }

    def create(self, validated_data): # redefinition de la methode create pour creer un patient
        user_data = validated_data.pop('user')    

        user = UtilisateurSerializer.create(
            UtilisateurSerializer(), validated_data=user_data
        )

        # Create the patient instance
        patient = Patient.objects.create(
            user=user, **validated_data
        ) # creation du patient
        return patient

#serializer pour le radiologue
class RadiologueSerializer(serializers.ModelSerializer):
    user = UtilisateurSerializer()
    class Meta:
        model = Radiologue
        fields = ('id' , 'user' )
        