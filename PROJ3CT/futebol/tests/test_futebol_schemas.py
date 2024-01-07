import pytest
from pydantic import ValidationError

from PROJ3CT.futebol.schemas import JogadorIn, TimeIn


def test_novo_time_schema():
    time = TimeIn(
        nome="Juventus",
    )
    assert time.nome == "Juventus"


def test_novo_jogador_valido_dezesseis_anos_schema():
    jogador = JogadorIn(
        nome="Cristiano Ronaldo",
        idade=16,
        time=0,
    )
    assert jogador.nome == "Cristiano Ronaldo"
    assert jogador.idade == 16
    assert jogador.time == 0


def test_novo_jogador_valido_cinquenta_anos_schema():
    jogador = JogadorIn(
        nome="Cristiano Ronaldo",
        idade=50,
        time=0,
    )
    assert jogador.nome == "Cristiano Ronaldo"
    assert jogador.idade == 50
    assert jogador.time == 0


def test_novo_jogador_invalido_idade_menor_dezesseis_anos_schema():
    with pytest.raises(ValidationError):
        JogadorIn(
            nome="Cristiano Ronaldo",
            idade=15,
            time=0,
        )


def test_novo_jogador_invalido_idade_maior_cinquenta_anos_schema():
    with pytest.raises(ValidationError):
        JogadorIn(
            nome="Cristiano Ronaldo",
            idade=51,
            time=0,
        )
