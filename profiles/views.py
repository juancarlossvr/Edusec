from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.template import TemplateDoesNotExist
from .models import Escenario, PerfilUsuario, RespuestaUsuario, MensajeChat, Insignia, TerminoGlosario
from .forms import ParticipanteForm, RespuestaForm

def inicio_view(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            participante, created = PerfilUsuario.objects.get_or_create(nombre=nombre, defaults=form.cleaned_data)
            
            if not created:
                RespuestaUsuario.objects.filter(participante=participante).delete()
                participante.curso = form.cleaned_data['curso']
                participante.edad = form.cleaned_data['edad']
                participante.genero = form.cleaned_data['genero']
                participante.save()

            request.session['participante_id'] = participante.id
            request.session['participante_nombre'] = participante.nombre

            primer_escenario = Escenario.objects.order_by('pk').first()
            if primer_escenario:
                return redirect('profiles:escenario', pk=primer_escenario.pk)
            else:
                return redirect('profiles:final')
    else:
        form = ParticipanteForm()
    return render(request, 'profiles/inicio.html', {'form': form})

def escenario_view(request, pk):
    escenario = get_object_or_404(Escenario, pk=pk)
    participante_id = request.session.get('participante_id')

    if not participante_id:
        return redirect('profiles:inicio')
    
    participante = get_object_or_404(PerfilUsuario, pk=participante_id)

    total_escenarios = Escenario.objects.count()
    escenarios_completados = RespuestaUsuario.objects.filter(participante=participante).count()
    progreso = (escenarios_completados / total_escenarios) * 100 if total_escenarios > 0 else 0

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

    template_name = f'profiles/escenario_{escenario.tipo}.html'
    
    context = {
        'escenario': escenario,
        'form': form,
        'progreso': progreso,
        'escenario_actual': escenarios_completados + 1,
        'total_escenarios': total_escenarios,
    }
    
    try:
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        return render(request, 'profiles/escenario.html', context)

def final_view(request):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('profiles:inicio')
        
    participante = get_object_or_404(PerfilUsuario, pk=participante_id)
    respuestas = RespuestaUsuario.objects.filter(participante=participante).select_related('escenario')
    puntaje = respuestas.filter(es_correcta=True).count()
    total = respuestas.count()

    insignias_ganadas = []
    if puntaje == total and total > 0:
        insignia, _ = Insignia.objects.get_or_create(
            nombre="Maestro de la Ciberseguridad", 
            defaults={'descripcion': "Completaste la simulación con un puntaje perfecto.", 'icono': 'fas fa-crown'}
        )
        participante.insignias.add(insignia)
        insignias_ganadas.append(insignia)

    if puntaje >= total * 0.75 and total > 0:
        insignia, _ = Insignia.objects.get_or_create(
            nombre="Detective Digital", 
            defaults={'descripcion': "Lograste un puntaje sobresaliente.", 'icono': 'fas fa-search-plus'}
        )
        participante.insignias.add(insignia)
        insignias_ganadas.append(insignia)
    
    participante.puntaje_total += puntaje
    participante.save()

    context = {
        'participante': participante,
        'puntaje': puntaje,
        'total': total,
        'respuestas': respuestas,
        'insignias_ganadas': insignias_ganadas
    }
    return render(request, 'profiles/final.html', context)

def chatbot_view(request):
    mensaje_actual = None
    if request.method == 'POST':
        opcion_elegida_id = request.POST.get('user_choice')
        if opcion_elegida_id:
            try:
                mensaje_actual = get_object_or_404(MensajeChat, pk=int(opcion_elegida_id))
            except (ValueError, MensajeChat.DoesNotExist):
                mensaje_actual = get_object_or_404(MensajeChat, pk=1)
        else:
            mensaje_actual = get_object_or_404(MensajeChat, pk=1)
    else:
        mensaje_actual = get_object_or_404(MensajeChat, pk=1)

    return render(request, 'profiles/chatbot.html', {'current_message': mensaje_actual})

def glosario_view(request):
    terminos = TerminoGlosario.objects.all()
    context = {
        'terminos': terminos
    }
    return render(request, 'profiles/glosario.html', context)

def perfil_view(request):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('profiles:inicio')

    participante = get_object_or_404(PerfilUsuario, pk=participante_id)
    
    todas_las_insignias = Insignia.objects.all()
    insignias_ganadas_ids = set(participante.insignias.values_list('id', flat=True))
    total_simulaciones = RespuestaUsuario.objects.filter(participante=participante).values('escenario').distinct().count()

    context = {
        'participante': participante,
        'todas_las_insignias': todas_las_insignias,
        'insignias_ganadas_ids': insignias_ganadas_ids,
        'total_simulaciones': total_simulaciones,
    }
    return render(request, 'profiles/perfil.html', context)

def ranking_view(request):
    participantes = PerfilUsuario.objects.filter(puntaje_total__gt=0).order_by('-puntaje_total')[:100]
    context = {
        'participantes': participantes
    }
    return render(request, 'profiles/ranking.html', context)

def generar_certificado_pdf(request):
    participante_id = request.session.get('participante_id')
    if not participante_id:
        return redirect('profiles:inicio')

    participante = get_object_or_404(PerfilUsuario, pk=participante_id)
    respuestas = RespuestaUsuario.objects.filter(participante=participante)
    puntaje = respuestas.filter(es_correcta=True).count()
    total = respuestas.count()
    
    fecha_actual = datetime.date.today().strftime("%d de %B de %Y")

    context = {
        'participante': participante,
        'puntaje': puntaje,
        'total': total,
        'fecha': fecha_actual,
    }

    html_string = render_to_string('profiles/certificado.html', context)
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado-edusec-{participante.nombre}.pdf"'
    
    return response