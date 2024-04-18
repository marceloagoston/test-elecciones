from django import forms

from .models import PoliticalParty


class PoliticalPartyForm(forms.ModelForm):
    class Meta:
        model = PoliticalParty
        fields = ['party_number', 'party_name', 'president', 'vice_president', 'slogan']
        labels = {
            'party_number': 'Nro. de Partido*',
            'party_name': 'Nombre del Partido',
            'president': 'Presidente',
            'vice_president': 'Vice Presidente',
            'slogan': 'Eslogan',
        }

        widgets = {
            'party_number': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del partido político',
                }
            ),
            'party_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del partido político',
                }
            ),
            'president': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre y apellido del / la Presidente de la lista',
                }
            ),
            'vice_president': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre y apellido del Vice-Presidente de la lista',
                }
            ),
            'slogan': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ingrese el eslogan del partido'}
            ),
        }
