import re
from datetime import datetime
from decimal import Decimal
from typing import Optional


def format_string(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().upper()


def cpf(value: str) -> str:
    value = value.strip()

    # se o CPF estiver no formato xxx.xxx.xxx-xx, retorna o mesmo
    if len(value) == 14:
        if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", value):
            raise ValueError(
                "CPF deve estar no formato xxx.xxx.xxx-xx ou apenas números."
            )
        return value

    if len(value) != 11:
        raise ValueError("CPF deve conter 11 dígitos.")
    if not value.isdigit():
        raise ValueError("CPF deve conter apenas dígitos.")

    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"


def nome(value: str) -> str:
    value = format_string(value)

    # Não sei qual é o menor nome possível, portanto, o mínimo é 1 caractere.
    if len(value) == 0:
        raise ValueError("Nome não pode estar vazio.")

    return value


def endereco(value: str) -> Optional[str]:
    value = format_string(value)

    if len(value) == 0:
        return None

    return value


def salario(value: str) -> Decimal:
    value = value.strip()

    if re.match(r"^\d+,\d{2}$", value):
        return Decimal(value.replace(",", "."))

    raise ValueError("Valor decimal inválido.")


def data(value: str) -> str:
    value = value.strip()

    try:
        datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida. Use o formato dd/mm/yyyy.")

    return value


def lote(value: str) -> int:
    value = value.strip()

    if not value.isdigit():
        raise ValueError("ID do lote deve conter apenas dígitos.")

    return int(value)


def telefone(value: str) -> Optional[str]:
    value = value.strip()

    if len(value) == 0:
        return None

    if not value.isdigit():
        raise ValueError("Telefone deve conter apenas dígitos.")

    return value


def email(value: str) -> Optional[str]:
    value = value.strip()

    if len(value) == 0:
        return None

    return value


def carteira(value: str) -> str:
    value = value.strip()

    if len(value) == 0:
        raise ValueError("")

    return value


def vinculo(value: str) -> str:
    value = value.strip()

    if len(value) == 0:
        raise ValueError("")

    return value


def funcao(value: str) -> str:
    value = value.strip()

    if len(value) == 0:
        raise ValueError("")

    return value
