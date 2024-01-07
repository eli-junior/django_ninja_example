import pytest
from django.db import transaction
from django.db.utils import IntegrityError

from PROJ3CT.futebol.models import Jogador, Time
from PROJ3CT.futebol.services.factories import jogador_factory, time_factory


def _cadastrar_time_db(qtty: int = 1):
    times = []
    novo_time = time_factory(qtty=qtty)
    for t in novo_time:
        time = Time.objects.get_or_create(nome=t.nome)
        times.append(time[0])
    return times


@pytest.mark.django_db
def test_request_buscar_todos_os_times_sem_times_retorna_404(client):
    response = client.get("/api/v1/futebol/times")
    print(response.json())
    assert response.status_code == 404


@pytest.mark.django_db
def test_request_buscar_todos_os_times_com_1_cadastrado_retorna_200(client):
    _cadastrar_time_db()
    response = client.get("/api/v1/futebol/times")
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_buscar_todos_os_times_com_dez_cadastrados(client):
    lista_times = len(_cadastrar_time_db(10))
    response = client.get("/api/v1/futebol/times")
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


# @pytest.mark.django_db
# def test_request_criar_novo_time(client):
#     import json
#     headers = {"Content-Type": "application/json"}
#     data = dict(nome="Vasco")
#     response = client.post("/api/v1/futebol/time", body=data)
#     print(response.json())
#     assert response.status_code == 201
