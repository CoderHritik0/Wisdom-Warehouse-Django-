from django import forms
from .models import note, note_image

class NoteForm(forms.ModelForm):
    class Meta:
        model = note
        fields = ['title', 'description', 'tag', 'color', 'is_hidden']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Write your note here...'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note tag'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'is_hidden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class NoteImageForm(forms.ModelForm):
    class Meta:
        model = note_image
        fields = ['image']
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True,'class': 'form-control', 'type': 'file'}),
        required=False,
    )
    