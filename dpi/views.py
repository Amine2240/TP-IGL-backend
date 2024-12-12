from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializer import ConsultationSerializer 


@api_view(['POST'])
#creer consultation 
def creer_consultation(request):
    consultation_serializer = ConsultationSerializer(
        data = request.data
    )   
    if consultation_serializer.is_valid():
        consultation_serializer.save()
        return Response(
            {"message":"La consultation a été créé avec succès" ,"consultation":consultation_serializer.data},
            status=status.HTTP_201_CREATED)
    return Response(consultation_serializer.errors , status=status.HTTP_400_BAD_REQUEST)