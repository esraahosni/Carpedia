from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Car, CarImage


class StyledUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-input',
                'placeholder': field.label,
            })
            field.help_text = ''


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'condition', 'model_name', 'year', 'price',
                  'engine', 'horsepower', 'fuel_type', 'transmission', 'description', 'main_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'main_image':
                field.widget.attrs.update({'class': 'form-input'})