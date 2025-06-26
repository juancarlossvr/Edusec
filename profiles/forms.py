from django import forms
from .models import PerfilUsuario, RespuestaUsuario, MensajeChat

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'curso', 'edad', 'genero'] # ¡Añade 'nombre' aquí!
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}), # Añade este widget
            'curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2° BTI'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 16'}),
            'genero': forms.Select(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre Completo o Apodo', 
            'curso': 'Curso',
            'edad': 'Edad',
            'genero': 'Género',
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = RespuestaUsuario
        fields = ['respuesta_dada']

class ChatForm(forms.ModelForm):
    class Meta:
        model = MensajeChat
        fields = ['texto', 'opciones', 'es_final']