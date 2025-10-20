from django import forms
from .models import note, note_image

class NoteForm(forms.ModelForm):
    class Meta:
        model = note
        fields = ['title', 'description', 'tag', 'color', 'is_hidden']

class NoteImageForm(forms.ModelForm):
    class Meta:
        model = note_image
        fields = ['image']