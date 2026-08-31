from django import forms
from .models import Order

FIELD_CLASS = 'form-control'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_type', 'event_date', 'location', 'message']
        widgets = {
            'service_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'event_date': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Ex: Dakar, Plateau'}),
            'message': forms.Textarea(attrs={'class': FIELD_CLASS, 'rows': 4,
                                             'placeholder': 'Décrivez votre projet...'}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'price']
        widgets = {
            'status': forms.Select(attrs={'class': FIELD_CLASS}),
            'price': forms.NumberInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Prix en FCFA'}),
        }