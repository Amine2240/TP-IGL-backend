from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from dpi.models import Hopital, HopitalUtilisateur
from utilisateur.forms import UtilisateurAdminForm
from utilisateur.models import (
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Patient,
    Radiologue,
    Utilisateur,
)

# Register your models here.
admin.site.register(Administratif)
admin.site.register(Infermier)
admin.site.register(Radiologue)
admin.site.register(Laborantin)
admin.site.register(Patient)

admin.site.site_header = "Gestion DPI"
admin.site.site_title = "Gestion DPI"
admin.site.index_title = "Welcome to your dashboard"


# Inline for managing users (doctors) associated with a hospital
class HopitalUtilisateurInline(admin.TabularInline):
    model = HopitalUtilisateur
    extra = 1  # Show one blank row for adding new relationships
    verbose_name = "User-Hospital Assignment"
    verbose_name_plural = "User-Hospital Assignments"


# Admin for Hopital (Hospital)
@admin.register(Hopital)
class HopitalAdmin(admin.ModelAdmin):
    list_display = ("nom", "lieu", "date_debut_service")
    search_fields = ("nom", "lieu")
    inlines = [HopitalUtilisateurInline]


# Admin for Utilisateur (User)
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "nom", "prenom", "role")
    search_fields = ("username", "email", "nom", "prenom")
    inlines = [HopitalUtilisateurInline]
    form = UtilisateurAdminForm


# Admin for Medecin
@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ("user", "specialite")
    search_fields = ("user__nom", "user__prenom", "specialite")


# Admin for HopitalUtilisateur (Intermediate Table)
@admin.register(HopitalUtilisateur)
class HopitalUtilisateurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "hopital", "date_adhesion")
    list_filter = ("hopital", "date_adhesion")
    search_fields = (
        "utilisateur__nom",
        "utilisateur__prenom",
        "hopital__nom",
    )

admin.site.site_header = "Gestion DPI"
admin.site.site_title = "Gestion DPI"
admin.site.index_title = "Welcome to your dashboard"