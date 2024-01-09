from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router

from .models import Jogador as JogadorDB
from .models import Time as TimeDB
from .schemas import ErrorResponse, TimeIn, TimeOut, JogadorIn, JogadorOut
from .services.normalize import padronizar_nome


router = Router()

# Time routes

@router.get("times", response={200: list[TimeOut], 204: None}, tags=["Time"])
def buscar_todos_os_times(request):
    try:
        times = get_list_or_404(TimeDB)
    except Http404:
        return 204, None
    return 200, times


@router.get("time/{id}", response={200: TimeOut, 404: ErrorResponse}, tags=["Time"])
def buscar_time_pelo_id(request, id: int):
    try:
        time = get_object_or_404(TimeDB, pk=id)
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    return 200, time


@router.get("time", response={200: TimeOut, 404: ErrorResponse}, tags=["Time"])
def buscar_time_pelo_nome(request, nome: str):
    try:
        time = get_object_or_404(TimeDB.objects.filter(nome=nome))
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    return 200, time


@router.post("time", response={201: TimeOut, 409: ErrorResponse}, tags=["Time"])
def cadastrar_novo_time(request, body: TimeIn):
    nome_interno = padronizar_nome(body.nome)
    if TimeDB.objects.filter(nome_interno=nome_interno).exists():
        return 409, ErrorResponse(detail="Time já cadastrado na base de dados")
    return 201, TimeDB.objects.create(nome=body.nome, nome_interno=nome_interno)


@router.put("time/{id}", response={200: TimeOut, 404: ErrorResponse}, tags=["Time"])
def atualizar_time(request, id: int, body: TimeIn):
    try:
        time = get_object_or_404(TimeDB, pk=id)
    except Http404:
        return 404, ErrorResponse(detail="Time não encontrado")
    time.nome = body.nome
    time.nome_interno = padronizar_nome(body.nome)
    time.save()
    return 200, time

# Jogadores routes

@router.get("jogadores", response={200: list[JogadorOut], 204: None}, tags=["Jogadores"])
def buscar_todos_os_jogadores(request):
    try:
        jogadores = get_list_or_404(JogadorDB)
    except Http404:
        return 204, None
    return 200, jogadores


@router.get("jogador/{id}", response={200: JogadorOut, 404: ErrorResponse}, tags=["Jogador"])
def buscar_jogador_pelo_id(request, id: int):
    try:
        jogador = get_object_or_404(JogadorDB, pk=id)
    except Http404:
        return 404, ErrorResponse(detail="Jogador não encontrado")
    return 200, jogador


@router.get("jogador", response={200: JogadorOut, 404: ErrorResponse}, tags=["Jogador"])
def buscar_jogador_pelo_nome(request, nome: str):
    try:
        jogador = get_object_or_404(JogadorDB.objects.filter(nome=nome))
    except Http404:
        return 404, ErrorResponse(detail="Jogador não encontrado")
    return 200, jogador


@router.post("jogador", response={201: JogadorOut, 409: ErrorResponse, 404: ErrorResponse}, tags=["Jogador"])
def cadastrar_novo_jogador(request, body: JogadorIn):
    nome_interno = padronizar_nome(body.nome)
    if JogadorDB.objects.filter(nome_interno=nome_interno).exists():
        return 409, ErrorResponse(detail="Jogador já cadastrado na base de dados")
    if body.time:
        try:
            time = get_object_or_404(TimeDB, pk=body.time)
        except Http404:
            return 404, ErrorResponse(detail="Time não encontrado")
    else:
        time = None
    return 201, JogadorDB.objects.create(nome=body.nome, idade=body.idade, nome_interno=nome_interno, time=time)


@router.put("jogador/{id}", response={200: JogadorOut, 404: ErrorResponse}, tags=["Jogador"])
def atualizar_jogador(request, id: int, body: JogadorIn):
    try:
        attempt = "Jogador"
        jogador = get_object_or_404(JogadorDB, pk=id)
        attempt = "Time"
        time = get_object_or_404(TimeDB, pk=body.time)

    except Http404:
        return 404, ErrorResponse(detail=f"{attempt} não encontrado")
    jogador.nome = body.nome
    jogador.nome_interno = padronizar_nome(body.nome)
    jogador.idade = body.idade
    jogador.time = time
    jogador.save()
    return 200, jogador