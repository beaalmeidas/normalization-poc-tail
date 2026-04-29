import re
from .utils import clean_text, normalize_number


def extract_measurement_and_packaging(text: str):
    peso_volume = re.search(r"(\d+(?:\.\d+)?)\s*(ML|L|LT|LTS|G|GR|KG|QUILO|KILO)", text)
    dimensao = re.search(r"(\d+(?:\.\d+)?)\s*(MM|CM|M)", text)
    tipo_embalagem = re.search(r"(CX|PCT|FD|DZ)\s*(\d+)", text)
    unidade_simples = re.search(r"(\d+)\s*(UN|UND)", text)

    return {
        "peso_volume": peso_volume.groups() if peso_volume else None,
        "tipo_embalagem": tipo_embalagem.groups() if tipo_embalagem else None,
        "unidade_simples": unidade_simples.groups() if unidade_simples else None,
        "dimensao": dimensao.groups() if dimensao else None,
    }

def preprocess(text: str) -> dict:
    text = clean_text(text)
    text = normalize_number(text)

    medidas = extract_measurement_and_packaging(text)

    return {
        "raw": text,
        **medidas
    }