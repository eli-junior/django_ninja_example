from django.db import models


class Time(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome


class Jogador(models.Model):
    nome = models.CharField(max_length=100)
    time = models.ForeignKey("Time", on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome
