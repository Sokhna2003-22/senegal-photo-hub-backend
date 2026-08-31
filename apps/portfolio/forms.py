from django import forms
from .models import PortfolioAlbum, PortfolioPhoto

FIELD_CLASS = 'form-control'

class PortfolioAlbumForm(forms.ModelForm):
    class Meta:
        model = PortfolioAlbum
        fields = ['title', 'description', 'category', 'cover_image', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'description': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 3}),
            'category': forms.Select(attrs={'class': FIELD_CLASS}),
            'cover_image': forms.FileInput(attrs={'class': FIELD_CLASS}),
        }