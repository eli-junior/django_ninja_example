import unidecode


def padronizar_nome(nome):
    nome_sem_acento = unidecode.unidecode(nome)
    return nome_sem_acento.lower()
