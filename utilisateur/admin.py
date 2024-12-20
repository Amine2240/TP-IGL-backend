from django.contrib import admin

from utilisateur.models import Utilisateur

# Register your models here.
admin.site.register(Utilisateur)

admin.site.site_header = "Gestion DPI"
admin.site.site_title = "Gestion DPI"
admin.site.index_title = "Welcome to your dashboard"