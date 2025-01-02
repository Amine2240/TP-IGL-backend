import cloudinary.uploader
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from IGLBackend.authentication import CookieJWTAuthentication

from .models import Examen, Hopital


# fonction pour upload une image sur cloudinary
def upload_image_to_cloudinary(request):
    img = request.FILES.get("image")
    print(img)
    if not img:
        raise ValueError("Veuillez ajouter une image radiologique")
    try:
        uploaded_img = cloudinary.uploader.upload(img, folder="radiographie/")
    except Exception as e:
        print(e)
        raise ValueError("Erreur lors de l'ajout de l'image radiologique")
    print(uploaded_img.get("url"))
    return uploaded_img.get("url")


# valider l'existence d'un hopital


def valider_hopital(id):
    try:
        return Hopital.objects.get(id=id)
    except Hopital.DoesNotExist:
        raise ValidationError(f"L'hôpital n'existe pas.")


# maj examen
def maj_examen(examen, resultats):

<<<<<<< HEAD
    examen = get_object_or_404(Examen, id=pk_examen)
    print(examen)
=======
>>>>>>> integration/oussama
    if not resultats:
        raise ValidationError({"Erreur": "Les résultats d'examen sont obligatoires."})

    examen.resultats = resultats
    examen.traite = True
    examen.save()

    return examen


# decode token and return user id
def decode_token(request):
    auth = CookieJWTAuthentication()
    # Decode the token
    user, _ = auth.authenticate(request)
    if not user:
        raise AuthenticationFailed("Invalid token or user not found.")
    return user.id

