from django import forms

class CheckoutForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=120)
    apellido = forms.CharField(label="Apellido", max_length=120)
    direccion = forms.CharField(label="Dirección", max_length=255, widget=forms.Textarea(attrs={"rows": 2}))
    email = forms.EmailField(label="Correo electrónico")
    telefono = forms.CharField(label="Teléfono", max_length=30)
