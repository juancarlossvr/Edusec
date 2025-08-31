from django.contrib import admin
from .models import PerfilUsuario, Escenario, RespuestaUsuario, MensajeChat, Insignia, TerminoGlosario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'edad', 'genero', 'puntaje_total') 
    list_filter = ('curso', 'genero')
    search_fields = ('nombre', 'curso')

@admin.register(Escenario)
class EscenarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'respuesta_correcta')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'descripcion')

@admin.register(RespuestaUsuario)
class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('participante', 'escenario', 'respuesta_dada', 'es_correcta')
    list_filter = ('es_correcta', 'escenario__titulo', 'participante__curso') 
    search_fields = ('participante__nombre', 'escenario__titulo', 'respuesta_dada') 

@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ('remitente', 'texto', 'es_final') 
    list_filter = ('remitente', 'es_final')
    search_fields = ('remitente', 'texto')

@admin.register(Insignia)
class InsigniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono', 'descripcion')
    search_fields = ('nombre',)

@admin.register(TerminoGlosario)
class TerminoGlosarioAdmin(admin.ModelAdmin):
    list_display = ('termino', 'icono')
    search_fields = ('termino', 'definicion', 'ejemplo')