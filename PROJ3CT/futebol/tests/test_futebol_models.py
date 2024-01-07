import pytest

from PROJ3CT.futebol.models import Jogador, Time
from PROJ3CT.futebol.services.factories import jogador_factory, time_factory


@pytest.mark.django_db
def test_criar_time():
    novo_time = time_factory()[0]
    time = Time.objects.create(nome=novo_time.nome)
    assert Time.objects.count() == 1
    assert time.nome == novo_time.nome
    assert str(time) == novo_time.nome


@pytest.mark.django_db
def test_criar_jogador():
    novo_time = time_factory()[0]
    novo_jogador = jogador_factory()[0]
    time = Time.objects.create(nome=novo_time.nome)
    jogador = Jogador.objects.create(**novo_jogador._asdict(), time=time)
    assert Jogador.objects.count() == 1
    assert jogador.nome == novo_jogador.nome
    assert jogador.idade == novo_jogador.idade
    assert jogador.time == time
    assert str(jogador) == novo_jogador.nome
