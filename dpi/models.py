import base64
from enum import Enum
from io import BytesIO

import qrcode
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from utilisateur.models import (
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Patient,
    Radiologue,
    Utilisateur,
)

# Create your models here.


# Dpi Model
class Dpi(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="dossier_patient"
    )
    contact_urgence = models.ForeignKey(
        "ContactUrgence", on_delete=models.SET_NULL, null=True, related_name="dpis"
    )
    hopital_initial = models.OneToOneField(
        "Hopital", on_delete=models.SET_NULL, null=True
    )
    date_creation = models.DateField(
        default=timezone.now
    )  # automatiquement remplie lors de la creation du dpi
    qr_code = models.TextField(
        max_length=500, blank=True
    )  # On va le stocker sous le format base-64

    # methode pour generer un qr code pour le dpi
    def generate_qr_code(self):
        """Génère un QR Code pour le DPI et l'encode en Base64"""
        # Données à encoder dans le QR Code
        # data_to_encode = f"https://angular_site/dpi/{self.id}"  # Exemple de lien pour accéder à l'objet DPI
        data_to_encode = f"Patient: {self.patient.id}, Hopital: {self.hopital_initial.id if self.hopital_initial else 'N/A'}"

        # Générer le QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_encode)
        qr.make(fit=True)

        # Convertir en image
        img = qr.make_image(fill_color="black", back_color="white")

        # Sauvegarder l'image en mémoire sous forme de bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encoder l'image en Base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()

        # Stocker le QR Code encodé en Base64 dans le champ `qr_code`
        self.qr_code = img_base64
        self.save()


# Soin Model
class Soin(models.Model):
    nom = models.CharField(max_length=32)
    type = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.type}: {self.nom}"


class Mutuelle(models.Model):
    nom = models.CharField(max_length=100)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="mutuelles"
    )


class SoinInfermier(models.Model):
    soin = models.ForeignKey(Soin, on_delete=models.CASCADE)
    infermier = models.ForeignKey(Infermier, on_delete=models.CASCADE)


class DpiSoin(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    soin = models.ForeignKey(Soin, on_delete=models.CASCADE)
    hopital = models.ForeignKey("Hopital", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    observation = models.TextField(blank=True)


# Outil Model
class Outil(models.Model):
    nom = models.CharField(max_length=32)


# Resume model
class Resume(models.Model):
    consultation = models.ForeignKey("Consultation", on_delete=models.CASCADE)
    diagnostic = models.TextField(blank=True)
    date_prochaine_consultation = models.DateField(null=True)


class ResumeSymptomes(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="symptomes"
    )
    symptome = models.CharField(max_length=500)


class ResumeMesuresPrises(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="mesures")
    mesure = models.CharField(max_length=500)


# Consultation Model
class Consultation(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="consultations")
    hopital = models.ForeignKey("Hopital", on_delete=models.CASCADE)
    date_de_consultation = models.DateField(default=timezone.now)
    heure = models.TimeField(default=timezone.now)


class ConsultationMedecin(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)


# Medicament Model
class Medicament(models.Model):
    nom = models.CharField(max_length=32)


# Prescription model
class Prescription(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    ordonnance = models.ForeignKey("Ordonnance", on_delete=models.CASCADE)
    dose = models.CharField(max_length=10)
    duree = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    heure = models.TimeField(null=True)
    nombre_de_prises = models.IntegerField(validators=[MinValueValidator(1)], null=True)

    def __str__(self):
        return f"{self.nom}"


# Ordonnance Model
class Ordonnance(models.Model):
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name="ordonnances"
    )
    date_de_creation = models.DateField(default=timezone.now)


# Certificat Model
class Certificat(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="certificats")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="certificats"
    )
    date = models.DateField(default=timezone.now)
    contenu = models.TextField(blank=True)
    accorde = models.BooleanField(default=False)


# ConsultationOutil Model
class ConsultationOutil(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    outil = models.ForeignKey(Outil, on_delete=models.CASCADE)


# Bilan Enum
class TypeBilan(Enum):
    BIOLOGIQUE = "biologique"
    RADIOLOGIQUE = "radiologique"


# Examen Model
class Examen(models.Model):
    TYPES_BILAN = [(type.value, type.name.capitalize()) for type in TypeBilan]
    note = models.TextField()
    traite = models.BooleanField(default=False)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    resultats = models.TextField(max_length=500)
    type = models.CharField(
        max_length=32,
        choices=TYPES_BILAN,
    )


# Bilan biologique Model
class BilanBiologique(models.Model):
    laborantin = models.ForeignKey(
        Laborantin, on_delete=models.CASCADE, related_name="bilans"
    )
    examen = models.OneToOneField(
        Examen, on_delete=models.CASCADE, related_name="bilan"
    )


# Bilan radiologique Model
class BilanRadiologique(models.Model):
    radiologue = models.ForeignKey(
        Radiologue, on_delete=models.CASCADE, related_name="bilans"
    )
    examen = models.OneToOneField(
        Examen, on_delete=models.CASCADE, related_name="bilan"
    )
    images_radio = models.JSONField()  # pour stocker la liste de URL (cloud)


# Graphique de tendance Model
class GraphiqueTendance(models.Model):
    titre = models.CharField(max_length=50)
    x_donnees = models.JSONField()
    y_donnees = models.JSONField()
    bilan_biologique = models.OneToOneField(
        BilanBiologique, on_delete=models.CASCADE, related_name="graphiqus"
    )


#
class Parametre(models.Model):
    nom = models.CharField(max_length=50)


class ParametreValeur(models.Model):
    parametre = models.ForeignKey(Parametre, on_delete=models.CASCADE)
    bilan_biologique = models.ForeignKey(BilanBiologique, on_delete=models.CASCADE)
    valeur = models.CharField(max_length=100)


# Hopital Model
class Hopital(models.Model):
    nom = models.CharField(max_length=100)
    lieu = models.CharField(max_length=100)
    date_debut_service = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nom


class HopitalUtilisateur(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    date_adhesion = models.DateField(default=timezone.now)


class Hospitalisation(models.Model):
    date_entree = models.DateField(default=timezone.now)
    date_sortie = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    cree_par = models.ForeignKey(Administratif, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)


class Antecedant(models.Model):
    nom = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)


class BilanBiologiqueLaborantin(models.Model):
    laborantin = models.ForeignKey(Laborantin, on_delete=models.CASCADE)
    bilan_bio = models.ForeignKey(BilanBiologique, on_delete=models.CASCADE)


class BilanRadiologiqueRadiologue(models.Model):
    radiologue = models.ForeignKey(Radiologue, on_delete=models.CASCADE)
    bilan_rad = models.ForeignKey(BilanRadiologique, on_delete=models.CASCADE)


class ContactUrgence(models.Model):
    nom = models.CharField(max_length=32)
    prenom = models.CharField(max_length=32)
    email = models.EmailField()
    telephone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Numero de telephone invalide",
            )
        ],
    )


class Decompte(models.Model):
    tarif = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(default=timezone.now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
