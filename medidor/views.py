import random
from django.shortcuts import render
from .models import FlujoAgua
from django.db.models import Avg  # Importar la función para obtener el promedio
from django.db.models import Sum #

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


# Nueva vista para mostrar el promedio y total de consumo
def promedio_consumo_view(request):
    # Calcular el promedio de consumo
    promedio_consumo = FlujoAgua.objects.aggregate(Avg('flujo_litros'))['flujo_litros__avg']
    if promedio_consumo is not None:
        promedio_consumo = round(promedio_consumo, 2)  # Redondear a dos decimales
    
    # Calcular el total de litros consumidos
    total_litros = FlujoAgua.objects.aggregate(Sum('flujo_litros'))['flujo_litros__sum']
    if total_litros is not None:
        total_litros = round(total_litros, 2)  # Redondear a dos decimales
    
    context = {
        'promedio_consumo': promedio_consumo,
        'total_litros': total_litros,
    }
    
    return render(request, 'medidor/promedio_consumo.html', context)