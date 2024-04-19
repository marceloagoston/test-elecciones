from django import forms
from django.core.exceptions import ValidationError

from .models import PoliticalParty, Voter

from .utils import can_vote


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


class VoterForm(forms.ModelForm):
    updating = False

    class Meta:
        model = Voter
        fields = ['last_name', 'first_name', 'dni', 'birth_date', 'district']
        labels = {
            'last_name': 'Apellido*',
            'first_name': 'Nombre*',
            'dni': 'DNI*',
            'birth_date': 'Fecha Nacimiento*',
            'district': 'Distrito*',
        }

        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el apellido del votante',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del votante',
                }
            ),
            'dni': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el DNI del votante',
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Ingrese fecha de nacimiento',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].widget.attrs['class'] = 'form-control'

    def clean_birth_date(self):
        """Validar si edad de votante elegida es mayor a 18 años"""
        if not can_vote(self.cleaned_data['birth_date']):
            raise ValidationError(
                'La persona debe tener mas de 18 años para poder registrarse como votante'
            )

        return self.cleaned_data['birth_date']

    def clean_dni(self):
        """Validar si DNI es válido y único"""
        instance = getattr(self, 'instance', None)
        dni_exclude = instance.dni if instance else None

        if self.cleaned_data['dni'] < 1000000 or self.cleaned_data['dni'] > 99999999:
            raise ValidationError('Debe ingresar un DNI válido')

        if Voter.objects.filter(dni=self.cleaned_data['dni']).exclude(dni=dni_exclude).exists():
            raise ValidationError('Ya existe un votante con ese DNI')

        return self.cleaned_data['dni']
