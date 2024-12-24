# Register your models here.
from django.contrib import admin

from dpi.models import ContactUrgence, Dpi, Hopital, Medicament, Soin

admin.site.register(Soin)
admin.site.register(Medicament)
admin.site.register(Dpi)
admin.site.register(ContactUrgence)
