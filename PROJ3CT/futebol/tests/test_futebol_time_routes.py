import pytest
from django.urls import reverse

from PROJ3CT.futebol.models import Time
from PROJ3CT.futebol.services.factories import time_factory


CONTENT_TYPE = "application/json"


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
    data = {"nome": "Vasco da Gama"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=CONTENT_TYPE)
    assert response.status_code == 201


@pytest.mark.django_db
def test_request_criar_novo_time_json_resposta(client):
    data = {"nome": "Vasco da Gama"}
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=CONTENT_TYPE)
    assert response.json() == {"id": 1, "nome": "Vasco da Gama"}


@pytest.mark.django_db
def test_request_criar_novo_time_com_nome_ja_cadastrado(client):
    data = {"nome": "Vasco da Gama"}
    client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=CONTENT_TYPE)
    response = client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=CONTENT_TYPE)
    assert response.status_code == 409


@pytest.mark.django_db
def test_atualizar_time_com_sucesso(client, subtests):
    data = {"nome": "Vasco"}
    client.post(reverse("api-1.0.0:cadastrar_novo_time"), data, content_type=CONTENT_TYPE)

    data = {"nome": "Vasco da Gama"}
    response = client.put(reverse("api-1.0.0:atualizar_time", args=[1]), data, content_type=CONTENT_TYPE)

    tests = (
        (response.status_code, 200),
        (response.json(), {"id": 1, "nome": "Vasco da Gama"}),
    )
    for entrada, saida in tests:
        with subtests.test(msg="Testa os dados do time atualizado", entrada=entrada, saida=saida):
            assert entrada == saida


@pytest.mark.django_db
def test_atualizar_time_com_id_inexistente(client, subtests):
    data = {"nome": "Vasco da Gama"}
    response = client.put(reverse("api-1.0.0:atualizar_time", args=[1]), data, content_type=CONTENT_TYPE)
    tests = (
        (response.status_code, 404),
        (response.json(), {"detail": "Time não encontrado"}),
    )

    for entrada, saida in tests:
        with subtests.test(msg="Não atualiza o time se o id não existe", entrada=entrada, saida=saida):
            assert entrada == saida
