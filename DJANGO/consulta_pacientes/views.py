# consulta_pacientes/views.py
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import pacientes, Consultas, CuentaRestaurante
from django.http import JsonResponse


def buscar_paciente(request):
    if request.method == 'POST':
        numero_paciente = request.POST.get('numero_paciente')
        nombre_paciente = request.POST.get('nombre_paciente')

        try:
            paciente = pacientes.objects.get(id_paciente=numero_paciente, nombre=nombre_paciente)
            consultas = Consultas.objects.filter(id_paciente=paciente, fecha_consulta__isnull=False)
            return render(request, 'resultados_consultas.html', {'paciente': paciente, 'consultas': consultas})
        except pacientes.DoesNotExist:
            mensaje = 'No se encontró ningún paciente con ese número y nombre.'
            return render(request, 'buscar_paciente.html', {'mensaje': mensaje})

    return render(request, 'buscar_paciente.html')

def qr_reader(request):
    return render(request, 'qr_reader.html')

def process_qr_code(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        try:
            qr_data_dict = json.loads(qr_data)

            nuevo_registro = CuentaRestaurante(
                id_restaurante=qr_data_dict.get('id_restaurante'),
                fecha_pedido=qr_data_dict.get('fecha_pedido'),
                precio_total=qr_data_dict.get('precio_total'),
                puntos_pedido=qr_data_dict.get('puntos_pedido')
            )

            nuevo_registro.save()
            return JsonResponse({'status': 'success', 'message': 'Datos del QR almacenados correctamente en la base de datos'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def nombre_restaurante(request):
    return render(request, 'nombre_restaurante.html')
