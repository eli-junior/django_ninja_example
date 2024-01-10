from collections import namedtuple
from random import randint, sample

from faker import Faker


time = namedtuple("Time", ["nome"])
jogador = namedtuple("Jogador", ["nome", "idade"])
fake = Faker("pt_BR")

TIMES = (
    "Atlético Mineiro",
    "Athletico Paranaense",
    "Avaí",
    "Botafogo",
    "Ceará",
    "Corinthians",
    "Coritiba",
    "Cuiabá",
    "Flamengo",
    "Fluminense",
    "Fortaleza",
    "Goiás",
    "Internacional",
    "Juventude",
    "Palmeiras",
    "Red Bull Bragantino",
    "Santos",
    "São Paulo",
    "Sport",
    "Vasco da Gama",
)


JOGADORES = (
    "Gabriel Silva",
    "Lucas Martins",
    "Matheus Carvalho",
    "Rafael Souza",
    "João Pereira",
    "Henrique Dias",
    "Gustavo Rocha",
    "Felipe Santos",
    "Daniel Oliveira",
    "Bruno Mendes",
    "Carlos Eduardo",
    "Marcelo Alves",
    "Thiago Moraes",
    "André Luiz",
    "Pedro Henrique",
    "Fernando Costa",
    "Ricardo Gomes",
    "Marcos Vinicius",
    "Alex Sandro",
    "Victor Hugo",
    "Eduardo Lima",
    "Roberto Carlos",
    "José Augusto",
    "Antônio Farias",
    "Joaquim Barbosa",
    "Leonardo Araújo",
    "Rodrigo Pacheco",
    "Caio Fernandes",
    "Diego Almeida",
    "Igor Ramos",
    "Lucas Gabriel",
    "Pedro Lucas",
    "Mateus Gomes",
    "Vinícius Teixeira",
    "Ricardo Oliveira",
    "André Santos",
    "José Eduardo",
    "Marcos Paulo",
    "Bruno Henrique",
    "Carlos Alberto",
    "Fabrício Melo",
    "Guilherme Silva",
    "Renato Carvalho",
    "Rodrigo Silva",
    "Lucas Rodrigues",
    "Miguel Fonseca",
    "Rafael Andrade",
    "João Vitor",
    "Luan Santana",
    "Caio César",
    "Fábio Júnior",
    "Gustavo Henrique",
    "Marcelo Ferreira",
    "Danilo Barros",
    "Eduardo Santos",
    "Paulo Roberto",
    "Tiago Ribeiro",
    "Fernando Araújo",
    "Victor Gabriel",
    "Diego Souza",
    "Alex Júnior",
    "Samuel Costa",
    "André Felipe",
    "Francisco Almeida",
    "Leandro Pereira",
    "Marcos Antônio",
    "Rafael Martins",
    "Carlos Henrique",
    "Luis Gustavo",
    "Pedro Miguel",
    "Leonardo Martins",
    "Rodrigo Fernandes",
    "Guilherme Costa",
    "Renan Oliveira",
    "Gabriel Alves",
    "João Paulo",
    "Mateus Silva",
    "Felipe Augusto",
    "Vinicius Moura",
    "Lucas Franco",
    "Roberto Junior",
    "Antonio Carlos",
    "Bruno César",
    "Davi Lucas",
    "Eduardo Melo",
    "Fabio Santos",
    "Guilherme Almeida",
    "Hector Luiz",
    "Ivan Marques",
    "João Ricardo",
    "Kaique Oliveira",
    "Luan Pereira",
    "Marcos Silva",
    "Nicolas Castro",
    "Otávio Mendes",
    "Paulo Henrique",
    "Rafael Borges",
    "Samuel Silva",
    "Thiago Santos",
    "Victor Almeida",
)

# Agora, 'lista_de_jogadores' é uma lista Python contendo os nomes dos jogadores.


def time_factory(qtty: int = 1):
    if qtty <= 0 or qtty > len(TIMES):
        raise ValueError(f"Quantidade de times deve ser menor ou igual a {len(TIMES)}")
    return [time(t) for t in sample(TIMES, qtty)]


def jogador_factory(qtty: int = 1):
    if qtty <= 0 or qtty > len(JOGADORES):
        raise ValueError(f"Quantidade de jogadores deve ser menor ou igual a {len(JOGADORES)}")
    return [jogador(j, randint(18, 41)) for j in sample(JOGADORES, qtty)]
