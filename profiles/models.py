from django.db import models
from django.contrib.auth.models import User # Asumiendo que PerfilUsuario usa User

class PerfilUsuario(models.Model):
    
    nombre = models.CharField(max_length=100, help_text="Introduce tu nombre o un identificador único")
    curso = models.CharField(max_length=50)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10) 

    def __str__(self):
        return f"{self.nombre} ({self.curso}, {self.edad} años)" 

class Escenario(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    opciones = models.JSONField()
    respuesta_correcta = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

class RespuestaUsuario(models.Model):
    participante = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    escenario = models.ForeignKey(Escenario, on_delete=models.CASCADE)
    respuesta_dada = models.CharField(max_length=100)
    es_correcta = models.BooleanField()

    def __str__(self):
        return f"{self.participante.nombre} - {self.escenario.titulo}"
    
class MensajeChat(models.Model):
    remitente = models.CharField(max_length=50, default="Chatbot")
    texto = models.TextField()
    opciones = models.JSONField(blank=True, null=True)
    es_final = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.remitente}: {self.texto[:50]}..."

class InteraccionChat(models.Model):
    participante = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    mensaje_chatbot = models.ForeignKey(MensajeChat, on_delete=models.CASCADE, related_name='interacciones')
    respuesta_usuario = models.CharField(max_length=255, blank=True, null=True) # Lo que el usuario escribió o la opción que eligió
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participante} - Chat: {self.mensaje_chatbot.texto[:30]}"