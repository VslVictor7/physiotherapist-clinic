from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
]

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)
    birth = models.DateField(null=True)
    adress = models.TextField(max_length=255)
    cep = models.CharField(max_length=9)

# Create your models here.
