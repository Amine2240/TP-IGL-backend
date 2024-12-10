from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view



@api_view(['POST']) 
# creer un patient et dossier patient 
def creer_dpi(request):
    print(request.body)
