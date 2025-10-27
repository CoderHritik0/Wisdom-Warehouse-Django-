from django import forms
from .models import note, note_image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import User

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

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
            'id': 'floatingUsername'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email',
            'id': 'floatingEmail'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'id': 'floatingPassword1'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'id': 'floatingPassword2'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class AuthenticationForm(DjangoAuthForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username',
            'id': 'floatingUsername'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
            'id': 'floatingPassword'
        })