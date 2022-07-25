from django.contrib import admin
from .models import AdoptionRequest, Pet, Kind

admin.site.register(Pet)
admin.site.register(Kind)
admin.site.register(AdoptionRequest)

# Register your models here.
