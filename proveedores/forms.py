from django import forms

class mantenerProveedor(forms.Form):
    nit = forms.CharField(label='Nit', max_length=12)
    nombre = forms.CharField(label='Razon Social', max_length=300)
    email = forms.CharField(label='Correo Electronico', max_length=100)
