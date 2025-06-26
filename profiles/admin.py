from django.contrib import admin
from .models import PerfilUsuario, Escenario, RespuestaUsuario, MensajeChat


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'edad', 'genero') 
    list_filter = ('curso', 'genero')
    search_fields = ('nombre', 'curso', 'edad') # Ahora puedes buscar por nombre también

@admin.register(Escenario)
class EscenarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'respuesta_correcta')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('titulo',) # Filtro opcional por título del escenario

@admin.register(RespuestaUsuario)
class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('participante', 'escenario', 'respuesta_dada', 'es_correcta')
    # Permite filtrar por campos relacionados
    list_filter = ('es_correcta', 'escenario__titulo', 'participante__curso', 'participante__genero') 
    # Permite buscar por campos relacionados y la respuesta dada
    search_fields = ('participante__nombre', 'escenario__titulo', 'respuesta_dada') 

@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    # No hay campo 'next_message', así que mostramos los campos existentes
    list_display = ('remitente', 'texto', 'es_final', 'opciones') 
    list_filter = ('remitente', 'es_final')
    search_fields = ('remitente', 'texto')