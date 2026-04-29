import re

from config import UNITS_MAP
from .utils import clean_text, normalize_number


# extrai informações de medidas e embalagem dos dados crus
    # retorna um dicionário com cada ponto definido
    # caso algum não seja aplicável, retorna none
def extract_measurement_and_packaging(text: str):
    number = r"(\d+(?:[.,]\d+)?)"
    units = r"(ML|L|LT|LTS|G|GR|KG|QUILO|KILO|MM|CM|M|UN|UND|CX|PCT|FD|DZ)"

    peso_volume = re.search(rf"{number}\s*{units}", text)
    dimensao = re.search(rf"{number}\s*(MM|CM|M)", text)
    tipo_embalagem = re.search(r"(CX|PCT|FD|DZ)\s*(?:C\/\s*)?(\d+)", text)
    unidade_simples = re.search(r"(\d+)\s*(UN|UND)", text)
    multipack = re.search(rf"(\d+)\s*[xX]\s*{number}\s*{units}", text)

    return {
        "peso_volume": peso_volume.groups() if peso_volume else None,
        "tipo_embalagem": tipo_embalagem.groups() if tipo_embalagem else None,
        "unidade_simples": unidade_simples.groups() if unidade_simples else None,
        "dimensao": dimensao.groups() if dimensao else None,
        "multipack": multipack.groups() if multipack else None,
    }


# define quantidades e embalagem em pares número-unidade
def parse_measurements_and_packaging(medidas: dict):
    if medidas["tipo_embalagem"]:
        tipo, qtd = medidas["tipo_embalagem"]
        return int(qtd), tipo

    if medidas["unidade_simples"]:
        qtd, unidade = medidas["unidade_simples"]
        return int(qtd), unidade

    if medidas["multipack"]:
        qtd_pack, valor, unidade = medidas["multipack"]
        return int(qtd_pack), "UN"

    if medidas["peso_volume"]:
        valor, unidade = medidas["peso_volume"]
        return float(valor), unidade

    return 1, "UN"


# converte informações recebidas da função anterior para os padrões semânticos estabelecidos 
def normalize_unit(unit: str, quantity: float):
    singular, plural = UNITS_MAP.get(unit, (unit, unit))
    return singular if quantity == 1 else plural


def preprocess(text: str) -> dict:
    text = clean_text(text)
    text = normalize_number(text)

    medidas = extract_measurement_and_packaging(text)

    quantidade, unidade = parse_measurements_and_packaging(medidas)
    unidade = normalize_unit(unidade, quantidade)

    return {
        "raw": text,
        "quantidade": quantidade,
        "unidade": unidade,
        "medidas": medidas
    }
