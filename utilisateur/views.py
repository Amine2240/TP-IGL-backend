from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializer import PatientSerializer

@api_view(['POST'])
def creer_patient (request):
      print("request.data")
      patient_serializer = PatientSerializer(data = request.data)
      if patient_serializer.is_valid():
            patient_serializer.save()
            return Response({"message":"Le patient a été créé avec succès"}, status = status.HTTP_201_CREATED)
      return Response(patient_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
