from django.shortcuts import render, redirect, get_object_or_404
from .models import Escenario, PerfilUsuario, RespuestaUsuario, MensajeChat
from .forms import ParticipanteForm, RespuestaForm

def inicio_view(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            # Evita duplicados si el usuario ya existe
            nombre = form.cleaned_data['nombre']
            participante, created = PerfilUsuario.objects.get_or_create(nombre=nombre, defaults=form.cleaned_data)
            
            # Si no fue creado, actualiza sus datos y limpia respuestas previas
            if not created:
                RespuestaUsuario.objects.filter(participante=participante).delete() # Limpia para nueva simulación
                participante.curso = form.cleaned_data['curso']
                participante.edad = form.cleaned_data['edad']
                participante.genero = form.cleaned_data['genero']
                participante.save()

            request.session['participante_id'] = participante.id
            primer_escenario = Escenario.objects.order_by('id').first()
            if primer_escenario:
                return redirect('profiles:escenario', pk=primer_escenario.id)
            else:
                return redirect('profiles:final') # Si no hay escenarios, va a la página final
    else:
        form = ParticipanteForm()
    return render(request, 'profiles/inicio.html', {'form': form})

def escenario_view(request, pk):
    escenario = get_object_or_404(Escenario, pk=pk)
    participante_id = request.session.get('participante_id')

    if not participante_id:
        return redirect('profiles:inicio')
    
    participante = get_object_or_404(PerfilUsuario, pk=participante_id)

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta_dada = form.cleaned_data['respuesta_dada']
            es_correcta = respuesta_dada == escenario.respuesta_correcta
            RespuestaUsuario.objects.create(
                participante=participante,
                escenario=escenario,
                respuesta_dada=respuesta_dada,
                es_correcta=es_correcta
            )
            
            siguiente_escenario = Escenario.objects.filter(pk__gt=pk).order_by('pk').first()
            if siguiente_escenario:
                return redirect('profiles:escenario', pk=siguiente_escenario.pk)
            else:
                return redirect('profiles:final')
    else:
        form = RespuestaForm()
    
    return render(request, 'profiles/escenario.html', {'escenario': escenario, 'form': form})

def final_view(request):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('profiles:inicio')
        
    participante = get_object_or_404(PerfilUsuario, pk=participante_id)
    respuestas = RespuestaUsuario.objects.filter(participante=participante)
    puntaje = respuestas.filter(es_correcta=True).count()
    total = respuestas.count()
    half_total = total / 2 if total > 0 else 0

    return render(request, 'profiles/final.html', {
        'puntaje': puntaje,
        'total': total,
        'half_total': half_total,
    })

def chatbot_view(request):
    mensaje_actual = None
    if request.method == 'POST':
        # El usuario ha seleccionado una opción
        opcion_elegida_id = request.POST.get('user_choice')
        if opcion_elegida_id:
            try:
                # Intenta encontrar el siguiente mensaje basado en la opción
                mensaje_actual = get_object_or_404(MensajeChat, pk=int(opcion_elegida_id))
            except (ValueError, MensajeChat.DoesNotExist):
                # Si hay un error, vuelve al principio
                mensaje_actual = get_object_or_404(MensajeChat, pk=1)
        else:
            # Si no hay opción, vuelve al principio
            mensaje_actual = get_object_or_404(MensajeChat, pk=1)
    else:
        # Es la primera vez que se carga la página
        mensaje_actual = get_object_or_404(MensajeChat, pk=1)

    return render(request, 'profiles/chatbot.html', {'current_message': mensaje_actual})