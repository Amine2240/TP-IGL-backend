import random
import string
import bcrypt
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Utilisateur ,Patient 
from dpi.models import Dpi , ContactUrgence
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


#contact_urgence Serializer
class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgence
        fields = ('id' , 'nom' , 'prenom' , 'telephone' ,'email')
        extra_kwargs = {
            'nom' : {'required':True},
            'prenom' : {'required':True},
            'telephone' : {'required':True},
        }
    
    def create(self, validated_data):
        nom = validated_data.get('nom', None)
        prenom = validated_data.get('prenom', None)
        telephone = validated_data.get('telephone', None)
        if not nom:
            raise serializers.ValidationError("Le nom est obligatoire")
        if not prenom:
            raise serializers.ValidationError("Le prenom est obligatoire")
        if not telephone:
            raise serializers.ValidationError("Le telephone est obligatoire")
        try:
            contact_urgence = ContactUrgence.objects.get(nom=nom , prenom=prenom , telephone=telephone )
        except ContactUrgence.DoesNotExist:
            contact_urgence = super().create(validated_data)
        return contact_urgence
    


#serializer pour le patient
class PatientSerializer(serializers.ModelSerializer):#serializer pour le patient
    user = UtilisateurSerializer()
    contact_urgence = ContactUrgenceSerializer()
    class Meta:
        model = Patient
        fields = ('id' , 'NSS' , 'user' ,'mutuelle' ,'contact_urgence')
        extra_kwargs ={
            'NSS' : {'required':True} ,   
        }

    def create(self, validated_data): # redefinition de la methode create pour creer un patient
        user_data = validated_data.pop('user')
        contact_urgence_data = validated_data.pop('contact_urgence')    
        user = UtilisateurSerializer.create(
            UtilisateurSerializer(), validated_data=user_data
        )

        # Create the patient instance
        patient = Patient.objects.create(
            user=user, **validated_data
        ) # creation du patient

        contact_urgence = ContactUrgenceSerializer.create(
            ContactUrgenceSerializer(), validated_data=contact_urgence_data
        )# creation du contact d'urgence

        # Create the DPI instance
        dpi = Dpi.objects.create(
            patient=patient ,
            contact_urgence=contact_urgence
        )
        # Generate the QR Code for the DPI
        dpi.generate_qr_code()
        return patient

