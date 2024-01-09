import pytest
from django.urls import reverse

from PROJ3CT.futebol.models import Time
from PROJ3CT.futebol.services.factories import time_factory


def _cadastrar_time_db(qtty: int = 1):
    times = []
    novo_time = time_factory(qtty=qtty)
    for t in novo_time:
        time = Time.objects.get_or_create(nome=t.nome)
        times.append(time[0])
    return times


@pytest.mark.django_db
def test_request_buscar_todos_os_times_sem_times_retorna_204(client):
    response = client.get(reverse("api-1.0.0:buscar_todos_os_times"))

    assert response.status_code == 204


@pytest.mark.django_db
def test_request_buscar_todos_os_times_com_1_cadastrado_retorna_200(client):
    _cadastrar_time_db()
    response = client.get(reverse("api-1.0.0:buscar_todos_os_times"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_todos_os_times_com_dez_cadastrados(client):
    lista_times = len(_cadastrar_time_db(10))
    response = client.get(reverse("api-1.0.0:buscar_todos_os_times"))
    assert len(response.json()) == lista_times


@pytest.mark.django_db
def test_request_buscar_time_por_id_inexistente_retorna_404(client):
    response = client.get("/api/v1/futebol/time/1")
    assert response.status_code == 404


@pytest.mark.django_db
def test_request_buscar_time_por_id_com_1_cadastrado_retorna_200(client):
    _cadastrar_time_db()
    response = client.get("/api/v1/futebol/time/1")
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_time_por_id_com_1_cadastrado_json_resposta(client):
    time = _cadastrar_time_db()[0]
    response = client.get("/api/v1/futebol/time/1")
    assert response.json() == {"id": time.id, "nome": time.nome}


@pytest.mark.django_db
def test_request_buscar_time_por_nome_inexistente_retorna_404(client):
    response = client.get("/api/v1/futebol/time?nome=inexistente")
    assert response.status_code == 404


@pytest.mark.django_db
def test_request_buscar_time_por_nome_com_1_cadastrado_retorna_200(client):
    time = _cadastrar_time_db()[0]
    response = client.get(f"/api/v1/futebol/time?nome={time.nome}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_time_por_nome_com_1_cadastrado_json_resposta(client):
    time = _cadastrar_time_db()[0]
    response = client.get(f"/api/v1/futebol/time?nome={time.nome}")
    assert response.json() == {"id": time.id, "nome": time.nome}


@pytest.mark.django_db
def test_request_criar_novo_time_retorna_201(client):
    content_type = "application/json"
    data = {"nome": "Vasco da Gama"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=content_type)
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_criar_novo_time_json_resposta(client):
    content_type = "application/json"
    data = {"nome": "Vasco da Gama"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=content_type)
    assert response.json() == {"id": 1, "nome": "Vasco da Gama"}


@pytest.mark.django_db
def test_request_criar_novo_time_com_nome_ja_cadastrado(client):
    content_type = "application/json"
    data = {"nome": "Vasco da Gama"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=content_type)
    assert response.status_code == 201
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=content_type)
    assert response.status_code == 409


@pytest.mark.django_db
def test_atualizar_time_com_sucesso(client):
    content_type = "application/json"
    data = {"nome": "Vasco"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=content_type)
    assert response.status_code == 201
    data = {"nome": "Vasco da Gama"}
    response = client.put(reverse("api-1.0.0:atualizar_time", args=[1]), data, content_type=content_type)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "nome": "Vasco da Gama"}


@pytest.mark.django_db
def test_atualizar_time_com_id_inexistente(client):
    content_type = "application/json"
    data = {"nome": "Vasco da Gama"}
    response = client.put(reverse("api-1.0.0:atualizar_time", args=[1]), data, content_type=content_type)
    assert response.status_code == 404
    assert response.json() == {"detail": "Time não encontrado"}
