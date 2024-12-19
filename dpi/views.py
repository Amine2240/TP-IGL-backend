from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .serializer import  SoinSerializer , DpiSerializer
from .utils import upload_image_to_cloudinary

@api_view(['POST']) #decorateur pour la methode creer_patient
def creer_dpi(request):
      if request.method == 'POST':
            serializer = DpiSerializer(data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response({"message":"Le dossier patient a été créé avec succès", "dpi":serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


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
#ajouter bilan radiologique 
def ajouter_Bilan_radiologique(request):# la fonction n'est pas encore complete 
    try:
        url = upload_image_to_cloudinary(request)
        return Response({"message":"L'image a été ajoutée avec succès" ,"url":url}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)


 
