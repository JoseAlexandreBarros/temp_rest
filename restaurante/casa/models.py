
from django.db import models
from datetime import datetime

class Reservas(models.Model):
    horario_choices=(
        ('TR','Tarde'),
        ('MN','Manhã'),
        ('NO','Noite')
    )
    local_choices=(
        ('CN','Centro'),
        ('PR','Periferia')
    )
    nome=models.CharField(max_length=50)
    horarios=models.CharField(max_length=2 ,choices=horario_choices)
    locais=models.CharField(max_length=2 ,choices=local_choices)
    data_reserva = models.IntegerField(default=1)
    
    
    def __str__(self):
        return self.nome
    
class Carrinho(models.Model):
    usuario=models.CharField(max_length=50)
    identidade=models.IntegerField(default=1)
    atual=models.CharField(max_length=50,default='nulo')

    def __str__(self):
        return self.usuario