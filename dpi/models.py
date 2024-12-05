from enum import Enum

from django.db import models

from utilisateur.models import Laborantin, Medecin, Patient, Radiologue

# Create your models here.


# Dpi Model
class Dpi(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="dossier_patient"
    )
    qr_code = models.TextField(
        max_length=500, blank=True
    )  # On va le stocker sous le format base-64


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


# Outil Model
class Outil(models.Model):
    nom = models.CharField(max_length=32)


# Consultation Model
class Consultation(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="consultations")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="consultations"
    )
    date_de_consultation = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    outils = models.ManyToManyField(Outil, through="ConsultationOutil")


# Medicament Model
class Medicament(models.Model):
    nom = models.CharField(max_length=32)
    effets_secondaire = models.TextField(blank=True)


# Ordonnance Model
class Ordonnance(models.Model):
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name="ordonnances"
    )
    medicaments = models.ManyToManyField(Medicament, through="OrdonnanceMedicament")
    date_de_creation = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)


# Ordonnance_Medicament Model  --> table intermediare
class OrdonnanceMedicament(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    duree = models.DecimalField(max_digits=5, decimal_places=2)


# Certificat Model
class Certificat(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="certificats")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="certificats"
    )
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField()
    description = models.TextField(blank=True)


# ConsultationOutil Model
class ConsultationOutil(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    outil = models.ForeignKey(Outil, on_delete=models.CASCADE)


# Examen Model
class Examen(models.Model):
    note = models.TextField()
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
