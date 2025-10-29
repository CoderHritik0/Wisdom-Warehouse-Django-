from django.contrib import admin
from .models import note, note_image, Profile

# Register your models here.
admin.site.register(note)
admin.site.register(note_image)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pin')