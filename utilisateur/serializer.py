import random
import string
import bcrypt
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Utilisateur ,Patient 

Utilisateur = get_user_model()

class UtilisateurSerializer(serializers.ModelSerializer):
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
    
    def create(self , validated_data):
        print("data: ")
        role = validated_data.pop('role',None)
        if not role : 
            raise serializers.ValidationError("Le role est obligatoire")
        if not validated_data['email']:
            raise serializers.ValidationError("Le email est obligatoire")
        validated_data['username'] = validated_data['email']
        password = UtilisateurSerializer.generer_mot_de_passe()
        user = Utilisateur.objects.create_user(**validated_data ,role=role ,password = password)

        # pour creer un utilisateur avec un role specifique le mot de passe est generer aleatoirement
        return user.save()  

class PatientSerializer(serializers.ModelSerializer):
    user = UtilisateurSerializer()
    class Meta:
        model = Patient
        fields = ('id' , 'NSS' , 'user' ,'mutuelle' ,'contact_urgence')
        extra_kwargs ={
            'NSS' : {'required':True} ,
            'user':{'read_only':True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print("user data : ") 
        print(user_data)
       
        user = Utilisateur.objects.create(**user_data)
        print(user)
        # Create the patient instance
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

        
    