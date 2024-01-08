import pytest

from PROJ3CT.futebol.services.factories import jogador_factory, time_factory
from PROJ3CT.futebol.services.normalize import padronizar_nome


def test_normalize_name():
    assert padronizar_nome("São Paulo") == "sao paulo"
    assert padronizar_nome("São Paulo Futebol Clube") == "sao paulo futebol clube"


def test_time_factory_passando_nome():
    time = time_factory()
    assert len(time) == 1
    assert time[0].nome


def test_time_factory_passando_quantidade_maior_que_amostra():
    with pytest.raises(ValueError):
        time_factory(100000)


def test_jogador_factory_passando_nome():
    jogador = jogador_factory()
    assert len(jogador) == 1
    assert jogador[0].nome


def test_jogador_factory_passando_quantidade_maior_que_amostra():
    with pytest.raises(ValueError):
        jogador_factory(100000)
