import pytest

from PROJ3CT.futebol.models import Jogador, Time
from PROJ3CT.futebol.services.factories import jogador_factory, time_factory
from PROJ3CT.futebol.services.normalize import padronizar_nome



@pytest.mark.django_db
def test_criar_time(subtests):
    novo_time = time_factory()[0]
    time = Time.objects.create(nome=novo_time.nome, nome_interno=padronizar_nome(novo_time.nome))

    testes = (
        (Time.objects.count(), 1),
        (time.nome, novo_time.nome),
        (str(time), novo_time.nome),
    )

    for entrada, saida in testes:
        with subtests.test(msg='Testa os dados do time criado', entrada=entrada, saida=saida):
            assert entrada == saida


@pytest.mark.django_db
def test_criar_jogador(subtests):
    novo_time = time_factory()[0]
    novo_jogador = jogador_factory()[0]
    time = Time.objects.create(nome=novo_time.nome)
    jogador = Jogador.objects.create(**novo_jogador._asdict(), time=time)
    
    testes = (
        (Jogador.objects.count(), 1),
        (jogador.nome, novo_jogador.nome),
        (jogador.idade, novo_jogador.idade),
        (jogador.time, time),
        (str(jogador), novo_jogador.nome),
    )
    for entrada, saida in testes:
        with subtests.test(msg='Testa os dados do jogador criado', entrada=entrada, saida=saida):
            assert entrada == saida


@pytest.mark.django_db
def test_excluir_time_do_jogador_seta_para_nulo():
    novo_time = time_factory()[0]
    novo_jogador = jogador_factory()[0]
    time = Time.objects.create(nome=novo_time.nome)
    jogador = Jogador.objects.create(**novo_jogador._asdict(), time=time)
    time.delete()
    jogador.refresh_from_db()
    assert jogador.time is None