from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


# Roles Enum
class RoleEnum(Enum):
    ADMINISTRATIF = "administratif"
    PATIENT = "patient"
    MEDECIN = "medecin"
    INFERMIER = "infermier"
    RADIOLOGUE = "radiologue"
    LABORANTIN = "laborantin"


# Utilisateur Model
class Utilisateur(
    AbstractUser
):  # Pour l'authentification --> donc le mot de passe est inculu par defaut
    ROLE_CHOICES = [(role.value, role.name.capitalize()) for role in RoleEnum]

    # Additional fields
    nom = models.CharField(max_length=32)
    prenom = models.CharField(max_length=32)
    date_naissance = models.DateField()
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
    photo_profil = models.URLField(max_length=200, blank=True, null=True)
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=RoleEnum.PATIENT.value,
    )

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"


# Medecin Model
class Medecin(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="medecin"
    )
    specialite = models.CharField(max_length=64)

    def __str__(self):
        return f"Dr. {self.user.nom} {self.user.prenom}"


# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="patient"
    )
    NSS = models.CharField(max_length=32)
    mutuelle = models.CharField(max_length=32)
    contact_urgence = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Numero de telephone invalide",
            )
        ],
    )

    def __str__(self):
        return f"Patient: {self.user.nom} {self.user.prenom}"


# Administratif Model
class Administratif(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="administratif"
    )

    def __str__(self):
        return f"Administratif: {self.user.nom} {self.user.prenom}"


# Infermier Model
class Infermier(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="infermier"
    )

    def __str__(self):
        return f"Infermier: {self.user.nom} {self.user.prenom}"


# Radiologue Model
class Radiologue(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="radiologue"
    )

    def __str__(self):
        return f"Radiologue: {self.user.nom} {self.user.prenom}"


# Laborantin Model
class Laborantin(models.Model):
    user = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, related_name="laborantin"
    )

    def __str__(self):
        return f"Laborantin: {self.user.nom} {self.user.prenom}"
