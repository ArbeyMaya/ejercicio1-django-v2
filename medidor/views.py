import random
from django.shortcuts import render, redirect
from .models import FlujoAgua
from django.db.models import Avg  # Importar la función para obtener el promedio
from django.db.models import Sum #
from django import forms
from django.contrib import messages
from .forms import LímiteConsumoForm

def ver_datos_agua(request):
    registros = FlujoAgua.objects.all().order_by('-timestamp')
    return render(request, 'medidor/ver_datos.html', {'registros': registros})

def flujo_agua_simulado(fijo=False):
    if fijo:
        return 1.0  # Generar exactamente 1 litro por segundo
    else:
        return round(random.uniform(0.1, 1.5), 2)

def contador_litros_por_minuto(duracion_minutos=1, modo_fijo=False):
    total_litros = 0
    minutos_data = []
    
    for minuto in range(duracion_minutos):
        litros_minuto = 0
        segundos_data = []
        
        for segundo in range(60):
            flujo_segundo = flujo_agua_simulado(fijo=modo_fijo)
            litros_minuto += flujo_segundo
            total_litros += flujo_segundo
            segundos_data.append(flujo_segundo)

            # Guardar cada lectura de segundo en la base de datos
            FlujoAgua.objects.create(minuto=minuto + 1, segundo=segundo + 1, flujo_litros=flujo_segundo)
        
        minutos_data.append({
            'minuto': minuto + 1,
            'litros': litros_minuto,
            'segundos': segundos_data,
        })
    
    return minutos_data, total_litros

def contador_view(request):
    duracion_minutos = int(request.GET.get('minutos', 1))
    modo_fijo = 'fijo' in request.GET  # Revisar si el botón de "1 litro por segundo" fue presionado
    minutos_data, total_litros = contador_litros_por_minuto(duracion_minutos, modo_fijo)

    context = {
        'minutos_data': minutos_data,
        'total_litros': total_litros,
        'duracion_minutos': duracion_minutos,
    }
    
    return render(request, 'medidor/contador.html', context)


def promedio_consumo_view(request):
    # Calcular el promedio de consumo
    promedio_consumo = FlujoAgua.objects.aggregate(Avg('flujo_litros'))['flujo_litros__avg']
    if promedio_consumo is not None:
        promedio_consumo = round(promedio_consumo, 2)
    
    # Calcular el total de litros consumidos
    total_litros = FlujoAgua.objects.aggregate(Sum('flujo_litros'))['flujo_litros__sum']
    if total_litros is not None:
        total_litros = round(total_litros, 2)
    
    # Obtener el límite de consumo de la sesión
    límite_consumo = request.session.get('límite_consumo')
    if límite_consumo is not None and total_litros is not None:
        if total_litros > límite_consumo:
            messages.warning(request, f"¡Alerta! Has superado tu límite de consumo de {límite_consumo} litros.")
    
    context = {
        'promedio_consumo': promedio_consumo,
        'total_litros': total_litros,
        'límite_consumo': límite_consumo,
    }
    
    return render(request, 'medidor/promedio_consumo.html', context)

# Vista para establecer el límite de consumo
def establecer_límite_view(request):
    if request.method == 'POST':
        form = LímiteConsumoForm(request.POST)
        if form.is_valid():
            # Guardar el límite en la sesión
            request.session['límite_consumo'] = form.cleaned_data['límite_litros']
            return redirect('promedio_consumo_view')  # Redirigir a la vista del consumo

    else:
        # Cargar el formulario con el valor actual del límite en la sesión (si existe)
        límite_actual = request.session.get('límite_consumo', 0)
        form = LímiteConsumoForm(initial={'límite_litros': límite_actual})
    
    return render(request, 'medidor/limite.html', {'form': form})