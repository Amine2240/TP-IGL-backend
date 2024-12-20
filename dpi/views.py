from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from .serializer import   DpiSerializer , DpiSoinSerializer ,BilanRadiologiqueSerializer , ExamenSerializer
from .models import Examen
from django.forms.models import model_to_dict

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
    dpi_soin_serializer = DpiSoinSerializer(
        data = request.data 
    )
    if dpi_soin_serializer.is_valid():
        dpi_soin_serializer.save()
        return Response(
            {"message":"Le soin a été ajouté avec succès" ,"soin":dpi_soin_serializer.data},
            status=status.HTTP_201_CREATED)
    return Response(dpi_soin_serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
#ajouter bilan radiologique 
def ajouter_Bilan_radiologique(request , pk_examen ):
   
    try:
        examen = Examen.objects.get(id= pk_examen)
    except Examen.DoesNotExist: 
        return Response(
             {"ERREUR":"EXAMEN N'EXISTE PAS"}, status=status.HTTP_404_NOT_FOUND
        )
    
    resultats = request.data.get('examen[resultats]')
    if not resultats :
         return Response({"Erreur":"Les resultats d'examen sont obligatoire"} , status=status.HTTP_400_BAD_REQUEST)
    
    examen.resultats = resultats 
    examen.traite = True
    examen.save()
    data = {}
    data['radiologue_id'] = request.data.get('radiologue_id')

    # Retrieve all uploaded files for the 'images_radio' key
    data['images_radio'] = request.FILES.getlist('images_radio')

    data['examen'] = model_to_dict(examen)

    serializer_bilan_radiologique =  BilanRadiologiqueSerializer (
        data= data,
    ) 
    if serializer_bilan_radiologique.is_valid():
        bilan_radiologique = serializer_bilan_radiologique.save()
        bilan_radiologique.objects.update()
        return Response({"ok"},status=status.HTTP_200_OK)
    return Response(serializer_bilan_radiologique.errors , status=status.HTTP_400_BAD_REQUEST)
        
   
    


