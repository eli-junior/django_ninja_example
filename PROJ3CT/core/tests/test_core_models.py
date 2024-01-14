import pytest

from PROJ3CT.core.models import User


EMAIL = "admin@admin.com"
PASSWORD = "admin"
NAME = "Fulano de Tal"


@pytest.mark.django_db
def test_criar_usuario_e_superusuario_sem_email_retorna_valueerror(subtests):
    tests = (User.objects.create_superuser, User.objects.create_user)
    for func in tests:
        with subtests.test(msg="Testa se o email é obrigatório", func=func):
            with pytest.raises(ValueError):
                assert func(email="")


def create_db_user(email=None, password=None, name=None) -> User:
    return User.objects.create_user(
        email=email or EMAIL,
        password=password or PASSWORD,
        name=name or NAME,
    )


@pytest.mark.django_db
def test_criar_usuario_com_sucesso():
    assert create_db_user()


@pytest.mark.django_db
def test_criar_usuario_full_name_short_name_and_str(subtests):
    user = create_db_user()
    tests = (
        (user.get_full_name(), NAME),
        (user.get_short_name(), NAME),
        (str(user), EMAIL),
    )
    for entrada, saida in tests:
        with subtests.test(msg="Testa o nome do usuário", entrada=entrada, saida=saida):
            assert entrada == saida


@pytest.mark.django_db
def test_criar_usuario_sem_nome_short_name_retorna_email_name():
    user = User.objects.create_user(email="adminsemuser@admin.com", password="admin")
    assert user.get_short_name() == "adminsemuser"


@pytest.mark.django_db
def test_criar_superusuario():
    assert User.objects.create_superuser(
        email="admin@admin.com",
        password="admin",
    )
