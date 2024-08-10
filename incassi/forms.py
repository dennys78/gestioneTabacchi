from django import forms
from django.forms import inlineformset_factory
from datetime import datetime


from .models import (
    Incasso, Image, Dettagli, descMovimenti
)


class IncassoForm(forms.ModelForm):

    totaleCassa = forms.DecimalField(label='Totale Cassa', widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'id': 'g_totaleCassa', 'readonly': 'readonly' }))
    descrizione = forms.CharField(label='Esito controllo', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'descrizioneId', 'readonly': 'readonly' }))

    class Meta: 
        model = Incasso
        fields = ['data', 'descrizione', 'totaleCassa', 'incassoPresunto']

        
        widgets = {
            'data': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                       'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                },
            ),
            'incassoPresunto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'g_incassoPresunto',
                }
            ),
        }

        


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class DettagliForm(forms.ModelForm):

    movimento = forms.ModelChoiceField(queryset=descMovimenti.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Dettagli
        fields = '__all__'
        widgets = {
            
            'entrata': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': 0.01,
                    'name': "rigo",
                    'onchange': "calcolaTotale(this);",
                }
            ),
            'uscita': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': 0.01,
                    'onchange': "calcolaTotale(this);",
                    }
            ),
        }


DettagliFormSet = inlineformset_factory(
    Incasso, Dettagli, form=DettagliForm,
    extra=1, can_delete=False,
    can_delete_extra=False
)
ImageFormSet = inlineformset_factory(
    Incasso, Image, form=ImageForm,
    extra=1, can_delete=True,
    can_delete_extra=False
)