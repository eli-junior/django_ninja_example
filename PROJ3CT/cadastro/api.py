from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from ninja import Router, UploadedFile

from .models import Livro
from .schema import LivroIn, LivroOut


router = Router()


@router.get("/livro", response=list[LivroOut])
def listar(
    request,
):
    livros = Livro.objects.all()
    return livros


@router.get("/livro/{id}")
def listar_livro(request, id: int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)


@router.post("/livro", response=LivroOut)
def cadastrar_livro(request, livro: LivroIn):
    livro = Livro.objects.create(**livro.model_dump())
    return livro


@router.post("/file")
def upload_file(request, file: UploadedFile):
    print(file.size)
    print(file.read())
    return 1
