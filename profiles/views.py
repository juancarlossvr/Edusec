from django.shortcuts import render, redirect, get_object_or_404
from .models import Escenario, PerfilUsuario, RespuestaUsuario, MensajeChat
from .forms import ParticipanteForm, RespuestaForm

def inicio_view(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save()
            request.session['participante_id'] = participante.id
            # CAMBIO AQUI: Usar 'profiles:escenario'
            return redirect('profiles:escenario', pk=1)
    else:
        form = ParticipanteForm()
    return render(request, 'profiles/inicio.html', {'form': form})

def escenario_view(request, pk):
    escenario = get_object_or_404(Escenario, pk=pk)
    participante_id = request.session.get('participante_id')

    if not participante_id:
        # CAMBIO AQUI: Usar 'profiles:inicio'
        return redirect('profiles:inicio')
    
    participante = get_object_or_404(PerfilUsuario, pk=participante_id) 

    if request.method == 'POST':
        form = RespuestaForm(request.POST) 
        if form.is_valid():
            respuesta_dada = form.cleaned_data['respuesta_dada']

            # Verifica si la respuesta dada es una de las opciones válidas del escenario
            if respuesta_dada not in escenario.opciones.values():
                form.add_error('respuesta_dada', 'La opción seleccionada no es válida para este escenario.')
                return render(request, 'profiles/escenario.html', {
                    'escenario': escenario,
                    'form': form,
                })

            es_correcta = respuesta_dada == escenario.respuesta_correcta
            RespuestaUsuario.objects.create(
                participante=participante,
                escenario=escenario,
                respuesta_dada=respuesta_dada,
                es_correcta=es_correcta
            )
            siguiente = pk + 1
            if Escenario.objects.filter(pk=siguiente).exists():
                # CAMBIO AQUI: Usar 'profiles:escenario'
                return redirect('profiles:escenario', pk=siguiente)
            else:
                # CAMBIO AQUI: Usar 'profiles:final'
                return redirect('profiles:final')
    else:
        form = RespuestaForm() 
    
    return render(request, 'profiles/escenario.html', {
        'escenario': escenario,
        'form': form,
    })

def final_view(request):
    participante_id = request.session.get('participante_id')
    participante = get_object_or_404(PerfilUsuario, pk=participante_id) 
    respuestas = RespuestaUsuario.objects.filter(participante=participante)
    puntaje = respuestas.filter(es_correcta=True).count()
    total = respuestas.count()
    
    # Calcula la mitad del total aquí en la vista
    # Usamos float division, pero puedes usar // para división entera si prefieres
    half_total = total / 2 if total > 0 else 0 

    return render(request, 'profiles/final.html', {
        'puntaje': puntaje,
        'total': total,
        'half_total': half_total, # Pasamos la nueva variable a la plantilla
    })

def chatbot_view(request):
    current_message_id = request.session.get('current_chat_message_id')

    if not current_message_id:
        current_message = get_object_or_404(MensajeChat, pk=1)
        request.session['current_chat_message_id'] = current_message.id
    else:
        current_message = get_object_or_404(MensajeChat, pk=current_message_id)

    if request.method == 'POST':
        user_choice_id = request.POST.get('user_choice')

        if user_choice_id:
            try:
                next_message_id = int(user_choice_id)
                next_message = get_object_or_404(MensajeChat, pk=next_message_id)

                request.session['current_chat_message_id'] = next_message.id

                if next_message.es_final:
                    # CAMBIO AQUI: Usar 'profiles:chatbot' si la redirección sigue siendo a la misma vista
                    return render(request, 'profiles/chatbot.html', {
                        'current_message': next_message,
                        'is_chat_final': True
                    })
                else:
                    # CAMBIO AQUI: Usar 'profiles:chatbot'
                    return redirect('profiles:chatbot')
            except ValueError:
                pass # Manejar error si user_choice_id no es un entero válido
        else:
            pass # No se seleccionó ninguna opción, recargar la misma página o mostrar error

    return render(request, 'profiles/chatbot.html', {
        'current_message': current_message,
        'is_chat_final': current_message.es_final
    })