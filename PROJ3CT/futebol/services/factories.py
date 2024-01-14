from collections import namedtuple
from random import randint, sample

from .population import JOGADORES, TIMES


time = namedtuple("Time", ["nome"])
jogador = namedtuple("Jogador", ["nome", "idade"])


def valida_qtty(qtty: int, field: tuple, name_field: str):
    if qtty <= 0 or qtty > len(field):
        raise ValueError(f"Quantidade de {name_field} deve ser menor ou igual a {len(field)} e maior que 0")


def time_factory(qtty: int = 1):
    valida_qtty(qtty, TIMES, "times")
    return [time(t) for t in sample(TIMES, qtty)]


def jogador_factory(qtty: int = 1):
    valida_qtty(qtty, JOGADORES, "jogadores")
    return [jogador(j, randint(18, 41)) for j in sample(JOGADORES, qtty)]
