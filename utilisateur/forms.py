from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from utilisateur.models import (
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Radiologue,
    Utilisateur,
)


class UtilisateurAdminForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [
            "username",
            "email",
            "password",
            "nom",
            "prenom",
            "role",
            "telephone",
            "date_naissance",
            "photo_profil",
            "is_superuser",
            "is_active",
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Validate password using Django's validators
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(
                f"Password validation failed: {', '.join(e.messages)}"
            )

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.password and not user.password.startswith(
            ("pbkdf2_sha256$", "bcrypt$", "argon2$")
        ):
            user.password = make_password(user.password)

        user.save()

        """
        # Add role-specific logic after saving the user
        if user.role == "medecin":
            Medecin.objects.get_or_create(user=user)
        elif user.role == "infermier":
            Infermier.objects.get_or_create(user=user)
        elif user.role == "laborantin":
            Laborantin.objects.get_or_create(user=user)
        elif user.role == "radiologue":
            Radiologue.objects.get_or_create(user=user)
        elif user.role == "administratif":
            Administratif.objects.get_or_create(user=user)
"""
        return user
