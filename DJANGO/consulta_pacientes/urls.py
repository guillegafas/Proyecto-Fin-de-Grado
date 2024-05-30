# consulta_pacientes/urls.py
from django.urls import path
from .views import buscar_paciente, qr_reader, process_qr_code, nombre_restaurante

urlpatterns = [
    path('buscar/', buscar_paciente, name='buscar_paciente'),
    path('', buscar_paciente, name='buscar_paciente'),
    path('qr_reader/', qr_reader, name='qr_reader'),
    path('process_qr_code/', process_qr_code, name='process_qr_code'),
    path('nombre_restaurante/', nombre_restaurante, name='nombre_restaurante'),
]