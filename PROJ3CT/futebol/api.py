from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router

from .models import Jogador as JogadorDB
from .models import Time as TimeDB
from .schemas import TimeIn, TimeOut


router = Router(tags=["Futebol"])


@router.get("times", response=list[TimeOut])
def buscar_todos_os_times(request):
    return get_list_or_404(TimeDB)


@router.get("time/{id}", response=TimeOut)
def buscar_time_pelo_id(request, id: int):
    return get_object_or_404(TimeDB, pk=id)


@router.get("time", response=TimeOut)
def buscar_time_pelo_nome(request, nome: str):
    return get_object_or_404(TimeDB.objects.filter(nome=nome))


@router.post("time")
def cadastrar_novo_time(request, nome: TimeIn):
    print(request.body)
    print(nome)
    return 1
    return TimeDB.objects.get_or_create(nome=data.nome)[0]
