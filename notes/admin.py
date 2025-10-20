from django.contrib import admin
from .models import note, note_image

# Register your models here.
admin.site.register(note)
admin.site.register(note_image)