from django.db import models
from user.models import User

SPECIALTY_CHOICES = [
        ('ORTHO', 'Ortopedista'),
        ('NEURO', 'Neurológica'),
        ('CARDIO', 'Cardiopulmonar'),
        ('PEDIAT', 'Pediátrica'),
        ('GERIAT', 'Geriátrica'),
        ('SPORT', 'Desportiva'),
        ('OTHER','Outros'),
]


class Fisioterapist(models.Model):
   id = models.AutoField(primary_key=True)
   user = models.OneToOneField(User, on_delete=models.PROTECT)
   specialty = models.CharField(choices=SPECIALTY_CHOICES, max_length=18)
   email = models.EmailField(unique=True)
   phone_number = models.CharField(max_length=15, null=True, blank=True)

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(Fisioterapist, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField()
    time = models.TimeField()
    tipo_tratamento = models.CharField(choices=SPECIALTY_CHOICES, max_length=255)
    resumo_problemas = models.TextField(max_length=6000)

# Create your models here.
