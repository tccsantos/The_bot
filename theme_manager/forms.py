from django import forms
from .models import Theme


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = '__all__'
        labels = {
            'name': "Nome",
            'user': "Usuários",
            'is_padoru': "Tem Padoru?",
            'available': "Está disponível?"
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Angel Beats',
                'class': 'form-control'
            }),
            'user': forms.CheckboxSelectMultiple(),
            'is_padoru': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
