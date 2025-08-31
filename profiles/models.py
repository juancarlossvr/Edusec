from django.db import models

class Insignia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    icono = models.CharField(max_length=50, help_text="Clase de Font Awesome, ej: 'fas fa-shield-alt'")

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    nombre = models.CharField(max_length=100, help_text="Introduce tu nombre o un identificador único")
    curso = models.CharField(max_length=50)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    puntaje_total = models.IntegerField(default=0)
    insignias = models.ManyToManyField(Insignia, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.curso}, {self.edad} años)"

class Escenario(models.Model):
    TIPO_ESCENARIO = [
        ('email', 'Email de Phishing'),
        ('popup', 'Alerta de Malware'),
        ('chat', 'Chat de Ingeniería Social'),
        ('web', 'Página Web Falsa'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_ESCENARIO, default='email')
    titulo = models.CharField(max_length=100)
    descripcion = models.JSONField()
    opciones = models.JSONField()
    respuesta_correcta = models.CharField(max_length=100)
    feedback_correcto = models.CharField(max_length=255, default="¡Correcto! Bien hecho.")
    feedback_incorrecto = models.CharField(max_length=255, default="Esa no era la mejor opción.")

    def __str__(self):
        return self.titulo

class RespuestaUsuario(models.Model):
    participante = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='respuestas')
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
    
class TerminoGlosario(models.Model):
    termino = models.CharField(max_length=100)
    definicion = models.TextField()
    ejemplo = models.TextField(blank=True, null=True, help_text="Un ejemplo práctico del término.")
    icono = models.CharField(max_length=50, default='fas fa-question-circle', help_text="Clase de Font Awesome, ej: 'fas fa-shield-alt'")

    class Meta:
        verbose_name = "Término del glosario"
        verbose_name_plural = "Términos del glosario"
        ordering = ['termino']

    def __str__(self):
        return self.termino