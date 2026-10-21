from django import forms
from theme_manager.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'name': "Nome",
            'nickname': "Apelido",
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'João Paulo',
                'class': 'form-control'
            }),
            'nickname': forms.TextInput(attrs={
                'placeholder': 'O_beta',
                'class': 'form-control'
            }),
        }