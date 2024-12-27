# Register your models here.
from django.contrib import admin

from dpi.models import ContactUrgence, Dpi, Hopital, Medicament, Mutuelle, Outil, Soin

admin.site.register(Soin)
admin.site.register(Medicament)
admin.site.register(Dpi)
admin.site.register(ContactUrgence)
admin.site.register(Mutuelle)
admin.site.register(Outil)
