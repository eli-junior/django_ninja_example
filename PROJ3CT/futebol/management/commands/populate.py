from random import choice, randint

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db.utils import OperationalError

from PROJ3CT.futebol.models import Jogador, Time
from PROJ3CT.futebol.services.factories import JOGADORES, TIMES
from PROJ3CT.futebol.services.normalize import padronizar_nome


class Command(BaseCommand):
    help = "Popula times e jogadores no banco de dados"

    users_data = [
        {
            "username": "ana",
            "email": "ana@localhost",
            "password": "ana123",
            "first_name": "Ana",
            "last_name": "Ficticia",
        },
        {
            "username": "joao",
            "email": "joao@localhost",
            "password": "jao123",
            "first_name": "João",
            "last_name": "Imaginário",
        },
    ]

    categories_data = ["Café da manhã", "Almoço", "Jantar", "Sobremesa", "Lanche"]

    def recipe_data_exists(self):
        try:
            return Time.objects.count() > 0 or Jogador.objects.count() > 0
        except OperationalError as e:
            raise CommandError("Verifique se o modelo Recipes foi migrado corretamente e tente novamente!") from e

    def popular_times(self):
        if times := Time.objects.all():
            return times

        Time.objects.bulk_create([Time(nome=n, nome_interno=padronizar_nome(n)) for n in TIMES])
        return Time.objects.all()

    def popular_jogadores(self, times: list[Time]):
        if jogadores := Jogador.objects.all():
            return jogadores

        Jogador.objects.bulk_create(
            [
                Jogador(nome=n, idade=randint(18, 40), time=choice(times) if randint(0, 1) else None, nome_interno=padronizar_nome(n))
                for n in JOGADORES
            ]
        )
        return Jogador.objects.all()

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force",
            "-f",
            action="store_true",
            help="Limpa a tabela antes de populá-la (use com cuidado!)",
        )

    def handle(self, *args, **options):
        if self.recipe_data_exists():
            if not options["force"]:
                error = "Banco de dados não está vazio. Use --force para limpar a tabela antes de populá-la (use com cuidado!)"
                raise CommandError(error)

            Time.objects.all().delete()
            Jogador.objects.all().delete()
            self.stdout.write(self.style.WARNING("Tabelas 'Time' e 'Jogador' limpas!"))

        self.popular_jogadores(times=self.popular_times())

        self.stdout.write(self.style.SUCCESS(f"{len(JOGADORES)} Jogadores cadastrados com sucesso em {len(TIMES)} Times!"))
