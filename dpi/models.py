from django.db import models

from utilisateur.models import Medecin, Patient

# Create your models here.


# Dpi Model
class Dpi(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="dossier_patient"
    )
    qr_code = models.TextField(
        max_length=500, blank=True
    )  # On va le stocker sous le format base-64


# Consultation Model
class Consultation(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="consultations")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="consultations"
    )
    date_de_consultation = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)


# Medicament Model
class Medicament(models.Model):
    name = models.CharField(max_length=32)
    effets_secondaire = models.TextChoices(blank=True)


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
    duree = models.DecimalField()


# Certificat Model
class Certificat(models.Model):
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="certificats")
    medecin = models.ForeignKey(
        Medecin, on_delete=models.CASCADE, related_name="certificats"
    )
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField()
    description = models.TextField(blank=True)
