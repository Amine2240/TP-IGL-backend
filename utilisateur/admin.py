from django.contrib import admin

from dpi.models import Hopital, HopitalUtilisateur
from utilisateur.models import (
    Administratif,
    Infermier,
    Laborantin,
    Medecin,
    Radiologue,
    Utilisateur,
)

# Register your models here.
admin.site.register(Administratif)
admin.site.register(Infermier)
admin.site.register(Radiologue)
admin.site.register(Laborantin)

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
    list_display = ("nom", "lieu", "date_debut_service")  # Display key fields
    search_fields = ("nom", "lieu")  # Allow searching by name and location
    inlines = [HopitalUtilisateurInline]  # Add inline to manage users


# Admin for Utilisateur (User)
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "nom", "prenom")  # Display user fields
    search_fields = ("username", "email", "nom", "prenom")  # Search by key fields
    inlines = [HopitalUtilisateurInline]  # Add inline to manage hospitals


# Admin for Medecin
@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ("user", "specialite")  # Display linked user and specialty
    search_fields = ("user__nom", "user__prenom", "specialite")  # Allow searching


# Admin for HopitalUtilisateur (Intermediate Table)
@admin.register(HopitalUtilisateur)
class HopitalUtilisateurAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "hopital", "date_adhesion")  # Display relationship
    list_filter = ("hopital", "date_adhesion")  # Allow filtering by hospital and date
    search_fields = (
        "utilisateur__nom",
        "utilisateur__prenom",
        "hopital__nom",
    )  # Allow searching
