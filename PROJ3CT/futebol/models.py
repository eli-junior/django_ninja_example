from django.db import models

from .services.normalize import padronizar_nome


class Time(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    nome_interno = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.nome_interno = padronizar_nome(self.nome)
        super().save(*args, **kwargs)


class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    time = models.ForeignKey("Time", on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome
