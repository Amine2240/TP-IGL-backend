from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializer import ConsultationSerializer , HopitalSerializer , SoinSerializer
import cloudinary.uploader

@api_view(['POST'])
#ajouter des hopitaux par un administrateur du systeme 
def ajouter_hopitaux(request):

    hopital_serializer = HopitalSerializer(

        data=request.data , many=True
    )
    if hopital_serializer.is_valid():
        hopital_serializer.save()
        return Response(
            {"message":"Les hopitaux ont été ajoutés avec succès" ,"hopitaux":hopital_serializer.data},
            status=status.HTTP_201_CREATED)
    return Response(hopital_serializer.errors , status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST'])
#ajouter soin 
def ajouter_soin(request):
    soin_serializer = SoinSerializer(
        data = request.data 
    )
    if soin_serializer.is_valid():
        soin_serializer.save()
        return Response(
            {"message":"Le soin a été ajouté avec succès" ,"soin":soin_serializer.data},
            status=status.HTTP_201_CREATED)
    return Response(soin_serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def ajouter_Bilan_radiologique(request):
    print(request.data)
    print(request.FILES)
    img = request.FILES.get('Radiographie')
    if not img:
        return Response({"message":"Veuillez ajouter une image radiologique"}, status=status.HTTP_400_BAD_REQUEST)
    uploaded_img = cloudinary.uploader.upload(img, folder='radiographie/')
    print(uploaded_img)
    return Response({"message":"L'image radiologique a été ajoutée avec succès" ,"image":uploaded_img['url']}, status=status.HTTP_201_CREATED)