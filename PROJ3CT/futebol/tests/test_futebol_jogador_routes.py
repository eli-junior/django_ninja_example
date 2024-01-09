import pytest
from django.urls import reverse

from PROJ3CT.futebol.models import Jogador
from PROJ3CT.futebol.services.factories import jogador_factory


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
    content_type = "application/json"
    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=content_type)
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_criar_novo_jogador_json_resposta(client):
    content_type = "application/json"
    data = {"nome": "Fulano de Tal", "idade": 20}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=content_type)
    assert response.json() == {"id": 1, "nome": "Fulano de Tal", "idade": 20, "time": None}


@pytest.mark.django_db
def test_request_criar_novo_jogador_com_nome_ja_cadastrado(client):
    content_type = "application/json"
    data = {"nome": "Fulano de Tal", "idade": 20}
    client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=content_type)
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=content_type)
    assert response.status_code == 409


@pytest.mark.django_db
def test_request_criar_jogador_com_time_inexistente_retorna_404(client):
    content_type = "application/json"
    data = {"nome": "Fulano de Tal", "idade": 20, "time": 1}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_jogador"), data, content_type=content_type)
    assert response.status_code == 404
