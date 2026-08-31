from django import forms
from .models import ClientGallery, Photo

FIELD_CLASS = 'form-control'

class ClientGalleryForm(forms.ModelForm):
    class Meta:
        model = ClientGallery
        fields = ['title', 'description', 'client_name', 'client_email', 'cover_image', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 3}),
            'client_name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'client_email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
            'cover_image': forms.FileInput(attrs={'class': FIELD_CLASS}),
            'expires_at': forms.DateTimeInput(attrs={'class': FIELD_CLASS, 'type': 'datetime-local'}),
        }


class GalleryAccessForm(forms.Form):
    access_code = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center text-uppercase',
            'placeholder': 'Ex: AB12CD34',
            'style': 'letter-spacing: 5px; font-size: 1.5rem;'
        })
    )