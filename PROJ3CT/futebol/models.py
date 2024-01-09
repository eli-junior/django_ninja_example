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
    nome = models.CharField(max_length=40)
    nome_interno = models.CharField(max_length=40)
    idade = models.PositiveIntegerField()
    time = models.ForeignKey("Time", on_delete=models.SET_NULL, null=True, blank=True)

    unique_together = ("nome_interno", "idade")

    def __str__(self):
        return self.nome
