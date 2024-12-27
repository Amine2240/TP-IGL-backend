from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from .serializer import   DpiSerializer , DpiSoinSerializer ,BilanRadiologiqueSerializer , ExamenSerializer ,HospitalisationSerializer
from .models import Examen 
from utilisateur.models import Administratif , Radiologue , Infermier
from django.forms.models import model_to_dict
from rest_framework.exceptions import AuthenticationFailed
from .utils import maj_examen , decode_token

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
    
    try:
           user_id = decode_token(request=request)
    except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)
    print(user_id)
    data ={}
    data = request.data.copy()
    data.update({
          "infermier_id" :str(Infermier.objects.get(user_id=user_id).id)
    })
    print(data)

    dpi_soin_serializer = DpiSoinSerializer(
        data = data
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
           user_id = decode_token(request=request)
    except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)
    
    try:
        examen = maj_examen(pk_examen=pk_examen , resultats=request.data.get('examen[resultats]'))
    except ValidationError as e :
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Examen.DoesNotExist:
        return Response({"error": "Examen n'existe pas."}, status=status.HTTP_404_NOT_FOUND) 

    data = {
        "examen" : model_to_dict(examen) ,
        "radiologue_id" :Radiologue.objects.get(user_id=user_id).id,
        "images_radio" : request.FILES.getlist('images_radio'),
    }

    serializer_bilan_radiologique =  BilanRadiologiqueSerializer (
        data= data,
    ) 
    if serializer_bilan_radiologique.is_valid():
        bilan=serializer_bilan_radiologique.save()
        return Response(
             {"Message":"Le bilan a été ajouté avec succès" ,"Bilan":bilan},
               status=status.HTTP_200_OK
               )
    return Response(serializer_bilan_radiologique.errors , status=status.HTTP_400_BAD_REQUEST)
        
   
@api_view(['POST'])
#creer hospitalisation
def creer_hospitalisation(request , pk_patient):
   
    try:
           user_id = decode_token(request=request)
    except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=401)
    
    data={}
    data = request.data.copy()
    data.update({
    "patient_id": pk_patient, 
    "creer_par_id": Administratif.objects.get(user_id=user_id).id 
    })
    hospitalisation_serializer = HospitalisationSerializer(
        data = data
    )
    if hospitalisation_serializer.is_valid():
        hospitalisation_serializer.save()
        return Response(
            {"message":"L'hospitalisation a été créée avec succès" ,"hospitalisation":hospitalisation_serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(hospitalisation_serializer.errors , status=status.HTTP_400_BAD_REQUEST)