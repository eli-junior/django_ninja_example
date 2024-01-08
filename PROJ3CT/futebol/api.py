from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router

from .models import Jogador as JogadorDB
from .models import Time as TimeDB
from .schemas import ErrorResponse, TimeIn, TimeOut
from .services.normalize import padronizar_nome


router = Router(tags=["Futebol"])


@router.get("times", response={200: list[TimeOut], 204: None})
def buscar_todos_os_times(request):
    try:
        times = get_list_or_404(TimeDB)
    except Http404:
        return 204, None
    return 200, times


@router.get("time/{id}", response={200: TimeOut, 404: ErrorResponse})
def buscar_time_pelo_id(request, id: int):
    try:
        time = get_object_or_404(TimeDB, pk=id)
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    return 200, time


@router.get("time", response={200: TimeOut, 404: ErrorResponse})
def buscar_time_pelo_nome(request, nome: str):
    try:
        time = get_object_or_404(TimeDB.objects.filter(nome=nome))
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    return 200, time


@router.post("time", response={201: TimeOut, 409: ErrorResponse})
def cadastrar_novo_time(request, body: TimeIn):
    nome_interno = padronizar_nome(body.nome)
    if TimeDB.objects.filter(nome_interno=nome_interno).exists():
        return 409, ErrorResponse(detail="Time já cadastrado na base de dados")
    return 201, TimeDB.objects.create(nome=body.nome, nome_interno=nome_interno)


@router.put("time/{id}", response={200: TimeOut, 404: ErrorResponse})
def atualizar_time(request, id: int, body: TimeIn):
    try:
        time = get_object_or_404(TimeDB, pk=id)
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    time.nome = body.nome
    time.nome_interno = padronizar_nome(body.nome)
    time.save()
    return 200, time
