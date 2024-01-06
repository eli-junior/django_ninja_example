from ninja import ModelSchema, Schema

from .models import Livro


class LivroOut(Schema):
    id: int
    titulo: str
    descricao: str
    autor: str | None = None
    editora: str | None = None


class LivroIn(ModelSchema):
    class Config:
        model = Livro
        model_fields = ["titulo", "descricao"]
