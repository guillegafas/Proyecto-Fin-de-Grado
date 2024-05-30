# consulta_pacientes/models.py
from django.db import models

class pacientes(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    class Meta:
        db_table = 'pacientes'

class medicos(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'medicos'

class Consultas(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    id_medico = models.ForeignKey(medicos, on_delete=models.CASCADE, db_column='id_medico')
    id_paciente = models.ForeignKey(pacientes, on_delete=models.CASCADE, db_column='id_paciente')
    fecha_consulta = models.DateField()
    observaciones = models.TextField()

    def __str__(self):
        return f"Consulta {self.id_consulta} - Médico: {self.id_medico} - Paciente: {self.id_paciente}"
    class Meta:
        db_table = 'consultas'

class CuentaRestaurante(models.Model):
    id_restaurante = models.IntegerField()
    fecha_pedido = models.DateTimeField()
    precio_total = models.FloatField()
    puntos_pedido = models.IntegerField()

    class Meta:
        db_table = 'cuentarestaurante'

    def __str__(self):
        return f"Restaurante {self.id_restaurante} - Pedido en {self.fecha_pedido}"