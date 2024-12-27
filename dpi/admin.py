# Register your models here.
from django.contrib import admin

from dpi.models import  Medicament, Soin , Dpi , Consultation , Examen , BilanRadiologique

admin.site.register(Soin)
admin.site.register(Medicament)
admin.site.register(Examen)
admin.site.register(BilanRadiologique)
admin.site.register(Consultation)
admin.site.register(Dpi)
