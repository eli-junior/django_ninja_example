from ninja import Field, ModelSchema, Schema

from .models import Jogador, Time


class ErrorResponse(Schema):
    detail: str


class TimeIn(Schema):
    nome: str = Field(..., example="Red Bull Bragantino")


class TimeOut(ModelSchema):
    class Config:
        model = Time
        model_fields = ["id", "nome"]


class JogadorIn(Schema):
    nome: str = Field(..., example="Cristiano Ronaldo")
    idade: int = Field(..., example="40", gt=15, lt=51)
    time: int | None = Field(None, example=1)


class JogadorOut(ModelSchema):
    class Config:
        model = Jogador
        model_fields = ["id", "nome", "idade", "time"]
