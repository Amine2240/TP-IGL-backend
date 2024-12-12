from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializer import PatientSerializer

@api_view(['POST']) #decorateur pour la methode creer_patient
def creer_patient (request):
      print("request.data")
      patient_serializer = PatientSerializer(
            data = request.data
      )
      if patient_serializer.is_valid():
            patient_serializer.save() # sauvegarde du patient
            return Response(
                  {"message":"Le patient a été créé avec succès" ,"patient":patient_serializer.data},
                    status = status.HTTP_201_CREATED
                  )
      return Response(
            patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST
         )
