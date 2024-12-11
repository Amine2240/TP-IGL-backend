# Register your models here.
from django.contrib import admin

from dpi.models import Hopital, Medicament, Soin

admin.site.register(Soin)
admin.site.register(Medicament)
