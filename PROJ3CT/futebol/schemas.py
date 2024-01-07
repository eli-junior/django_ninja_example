from ninja import Field, ModelSchema, Schema

from .models import Jogador, Time


class TimeIn(Schema):
    nome: str = Field(..., example="Red Bull Bragantino")


class TimeOut(TimeIn):
    id: int


class JogadorIn(Schema):
    nome: str = Field(..., example="Cristiano Ronaldo")
    idade: int = Field(..., example="40", gt=15, lt=51)
    time: int


# class JogadorOut(ModelSchema):
#     id: int
#     nome: str
#     idade: int
#     time: str

#     class Config:
#         from_orm = True


# class JogadorCreated(BaseModel):
#     message: str = "Jogador inserido com sucesso!"
#     jogador: JogadorOut
