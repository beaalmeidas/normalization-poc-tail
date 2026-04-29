import re

from .config import UNITS_MAP

# padroniza o texto para maiúsculo, remove espaços duplos ou no início e fim
def clean_text(text: str) -> str:
    text = text.upper()
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


# padroniza decimais para usarem ponto
def normalize_number(text: str) -> str:
    return text.replace(",", ".")


# converte informações de medida e embalagem recebidas do
    # pré-processamento para os padrões semânticos estabelecidos 
def normalize_unit(unit: str):
    if not unit:
        return None
    return UNITS_MAP.get(unit.upper(), (unit.upper(), unit.upper()))