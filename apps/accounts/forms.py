from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PhotographerProfile

FIELD_CLASS = 'form-control'

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': FIELD_CLASS}))
    role = forms.ChoiceField(
        choices=(
            ('photographer', 'Je suis Photographe'),
            ('client', 'Je suis Client'),
        ),
        widget=forms.RadioSelect
    )
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': FIELD_CLASS}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': FIELD_CLASS}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': FIELD_CLASS}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = FIELD_CLASS


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': FIELD_CLASS}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': FIELD_CLASS}))


class PhotographerProfileForm(forms.ModelForm):
    class Meta:
        model = PhotographerProfile
        fields = ['bio', 'city', 'website', 'instagram']