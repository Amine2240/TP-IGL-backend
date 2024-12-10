from enum import Enum
import qrcode
import base64
from io import BytesIO
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from utilisateur.models import (
    Administratif,
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
    hopital_initial = models.OneToOneField(
        "Hopital", on_delete=models.SET_NULL, null=True
    )
    qr_code = models.TextField(
        max_length=500, blank=True
    )  # On va le stocker sous le format base-64

    # methode pour generer un qr code pour le dpi
    def generate_qr_code(self):
        """Génère un QR Code pour le DPI et l'encode en Base64"""
        # Données à encoder dans le QR Code
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


# Soins Enum
class TypeSoin(Enum):
    TYPE_1 = "type_1"
    TYPE_2 = "type_2"
    TYPE_3 = "type_3"


# Soin Model
class Soin(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="soins")
    TYPES_SOINS = [(type.value, type.name.capitalize()) for type in TypeSoin]
    type = models.CharField(
        max_length=32,
        choices=TYPES_SOINS,
        default=TypeSoin.TYPE_1.value,
    )
    date = models.DateField(auto_now_add=True)
    observation = models.TextField(blank=True)
    coup = models.DecimalField(max_digits=5, decimal_places=2)


class DpiSoin(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE)
    soin = models.ForeignKey(Soin, on_delete=models.CASCADE)


# Outil Model
class Outil(models.Model):
    nom = models.CharField(max_length=32)


# Consultation Model
class Consultation(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="consultations")
    medecin_principal = models.ForeignKey(
        Medecin, on_delete=models.SET_NULL, null=True, related_name="consultations"
    )
    hopital = models.ForeignKey("Hopital", on_delete=models.CASCADE)
    date_de_consultation = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)


class ConsultationMedecin(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)


# Medicament Model
class Medicament(models.Model):
    nom = models.CharField(max_length=32)
    effets_secondaire = models.TextField(blank=True)


# Ordonnance Model
class Ordonnance(models.Model):
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name="ordonnances"
    )
    date_de_creation = models.DateField(auto_now_add=True)


# Ordonnance_Medicament Model  --> table intermediare
class OrdonnanceMedicament(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE)
    dose = models.CharField(max_length=10)
    duree = models.DecimalField(max_digits=5, decimal_places=2)
    heure = models.CharField(max_length=10)
    nombre_de_prises = models.IntegerField(validators=[MinValueValidator(1)])


# Certificat Model
class Certificat(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="certificats")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="certificats"
    )
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField()
    description = models.TextField(blank=True)
    accorde = models.BooleanField(default=False)


# ConsultationOutil Model
class ConsultationOutil(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    outil = models.ForeignKey(Outil, on_delete=models.CASCADE)


# Examen Model
class Examen(models.Model):
    note = models.TextField()
    traite = models.BooleanField(default=False)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)


# Bilan Enum
class TypeBilan(Enum):
    BIOLOGIQUE = "biologique"
    RADIOLOGIQUE = "radiologique"


# Bilan Model
class Bilan(models.Model):
    TYPES_BILAN = [(type.value, type.name.capitalize()) for type in TypeBilan]
    type = models.CharField(
        max_length=32,
        choices=TYPES_BILAN,
    )
    resultats = models.TextField(max_length=500)
    examen = models.OneToOneField(
        Examen, on_delete=models.CASCADE, related_name="bilan"
    )


# Bilan biologique Model
class BilanBiologique(models.Model):
    bilan = models.OneToOneField(
        Bilan, on_delete=models.CASCADE, related_name="bilan_biologique"
    )
    laborantin = models.ForeignKey(
        Laborantin, on_delete=models.CASCADE, related_name="bilans"
    )


# Bilan radiologique Model
class BilanRadiologique(models.Model):
    bilan = models.OneToOneField(
        Bilan, on_delete=models.CASCADE, related_name="bilan_radiologique"
    )
    radiologue = models.ForeignKey(
        Radiologue, on_delete=models.CASCADE, related_name="bilans"
    )
    images_radio = models.JSONField()  # pour stocker la liste de URL (cloud)


# Graphique de tendance Model
class GraphiqueTendance(models.Model):
    titre = models.CharField(max_length=50)
    x_donnees = models.JSONField()
    y_donnees = models.JSONField()
    bilan_biologique = models.OneToOneField(
        BilanBiologique, on_delete=models.CASCADE, related_name="graphique_tendance"
    )


# Hopital Model
class Hopital(models.Model):
    nom = models.CharField(max_length=64)
    lieu = models.CharField(max_length=64)
    date_debut_service = models.DateField(auto_now_add=True)


class HopitalUtilisateur(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    date_adhesion = models.DateField(auto_now_add=True)


class Hospitazliation(models.Model):
    date_entree = models.DateField(auto_now_add=False)
    date_sortie = models.DateField(auto_now_add=True)
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
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Numero de telephone invalide",
            )
        ],
    )


class Decompte(models.Model):
    tarif = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
