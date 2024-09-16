from django import forms

class LímiteConsumoForm(forms.Form):
    límite_litros = forms.FloatField(label='Límite de consumo (litros)')