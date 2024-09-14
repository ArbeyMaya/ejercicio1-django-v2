from django.db import models

class FlujoAgua(models.Model):
    minuto = models.IntegerField()
    segundo = models.IntegerField()
    flujo_litros = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Marca de tiempo cuando se guarda el registro

    def __str__(self):
        return f"Minuto {self.minuto}, Segundo {self.segundo}: {self.flujo_litros} litros"