import pytest
from django.urls import reverse

from PROJ3CT.futebol.models import Jogador
from PROJ3CT.futebol.services.factories import jogador_factory


CONTENT_TYPE = "application/json"


def _cadastrar_jogador_db(qtty: int = 1, time=None):
    jogadores = []
    novo_jogador = jogador_factory(qtty=qtty)
    for j in novo_jogador:
        jogador = Jogador.objects.get_or_create(nome=j.nome, idade=j.idade, time=time)
        jogadores.append(jogador[0])
    return jogadores


@pytest.mark.django_db
def test_request_buscar_todos_os_jogadores_sem_jogadores_retorna_204(client):
    response = client.get(reverse("api-1.0.0:buscar_todos_os_jogadores"))
    assert response.status_code == 204


@pytest.mark.django_db
def test_request_buscar_todos_os_jogadores_com_1_cadastrado_retorna_200(client):
    _cadastrar_jogador_db()
    response = client.get(reverse("api-1.0.0:buscar_todos_os_jogadores"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_jogador_por_id_inexistente_retorna_404(client):
    response = client.get("/api/v1/futebol/jogador/1")
    assert response.status_code == 404


@pytest.mark.django_db
def test_request_buscar_jogador_por_id_com_1_cadastrado_json_resposta(client):
    jogador = _cadastrar_jogador_db()[0]
    response = client.get("/api/v1/futebol/jogador/1")
    assert response.json() == {
        "id": jogador.id,
        "nome": jogador.nome,
        "idade": jogador.idade,
        "time": None,
    }


@pytest.mark.django_db
def test_request_buscar_jogador_por_nome_inexistente_retorna_404(client):
    response = client.get("/api/v1/futebol/jogador?nome=inexistente")
    assert response.status_code == 404


@pytest.mark.django_db
def test_request_buscar_jogador_por_nome_com_1_cadastrado_retorna_200(client):
    jogador = _cadastrar_jogador_db()[0]
    response = client.get(f"/api/v1/futebol/jogador?nome={jogador.nome}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_jogador_por_nome_com_1_cadastrado_json_resposta(client):
    jogador = _cadastrar_jogador_db()[0]
    response = client.get(f"/api/v1/futebol/jogador?nome={jogador.nome}")
    assert response.json() == {
        "id": jogador.id,
        "nome": jogador.nome,
        "idade": jogador.idade,
        "time": None,
    }


@pytest.mark.django_db
def test_request_criar_novo_jogador_retorna_201(client):
    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=CONTENT_TYPE)
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_criar_novo_jogador_json_resposta(client):
    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=CONTENT_TYPE)
    assert response.json() == {"id": 1, "nome": "Fulano de Tal", "idade": 20, "time": None}


@pytest.mark.django_db
def test_request_criar_novo_jogador_com_nome_ja_cadastrado(client):
    data = {"nome": "Fulano de Tal", "idade": 20}
    client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=CONTENT_TYPE)
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=CONTENT_TYPE)
    assert response.status_code == 409


@pytest.mark.django_db
def test_request_criar_jogador_com_time_inexistente_retorna_404(client):
    data = {"nome": "Fulano de Tal", "idade": 20, "time": 1}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=CONTENT_TYPE)
    assert response.status_code == 404


@pytest.mark.django_db
def test_atualizar_jogador_com_sucesso(client, subtests):
    _cadastrar_jogador_db()[0]

    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.put(reverse("api-1.0.0:atualizar_jogador", args=[1]), data, content_type=CONTENT_TYPE)

    tests = (
        (response.status_code, 200),
        (response.json(), {"id": 1, "nome": "Fulano de Tal", "idade": 20, "time": None}),
    )
    for entrada, saida in tests:
        with subtests.test(msg="Testa os dados do jogador atualizado"):
            assert entrada == saida


@pytest.mark.django_db
def test_atualizar_jogador_com_id_inexistente(client, subtests):
    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.put(reverse("api-1.0.0:atualizar_jogador", args=[1]), data, content_type=CONTENT_TYPE)
    tests = (
        (response.status_code, 404),
        (response.json(), {"detail": "Id do jogador não encontrado"}),
    )

    for entrada, saida in tests:
        with subtests.test(msg="Não atualiza o jogador quando o id não existe"):
            assert entrada == saida


@pytest.mark.django_db
def test_atualizar_jogador_com_id_do_time_inexistente(client, subtests):
    _cadastrar_jogador_db()[0]

    data = {"nome": "Fulano de Tal", "idade": 20, "time": 1}
    response = client.put(reverse("api-1.0.0:atualizar_jogador", args=[1]), data, content_type=CONTENT_TYPE)
    tests = (
        (response.status_code, 404),
        (response.json(), {"detail": "Id do time não encontrado"}),
    )

    for entrada, saida in tests:
        with subtests.test(msg="não atualiza o time do jogador quando o id do time não existe"):
            assert entrada == saida
