import re
from .config import TEMPLATE, UNIDADES_MAP, DEFAULT_COLOR


def normalize_unit(unit: str):
    if not unit:
        return None
    return UNIDADES_MAP.get(unit.upper(), unit)

def ensure_color(cor: str):
    return cor if cor else DEFAULT_COR

def validate_format(text: str):
    pattern = r".+ - \d+(\.\d+)? (MILILITROS|LITROS|GRAMAS|QUILOGRAMAS)"
    return bool(re.match(pattern, text))

def build_output(nome, marca, cor, extras, quantidade, unidade):
    cor = ensure_color(cor)
    unidade = normalize_unit(unidade)

    extras_str = f" {extras}" if extras else ""

    return f"{nome} {marca} {cor}{extras_str} - {quantidade} {unidade}"

def postprocess(llm_output: dict):
    nome = llm_output.get("nome")
    marca = llm_output.get("marca")
    cor = llm_output.get("cor")
    extras = llm_output.get("extras")
    quantidade = llm_output.get("quantidade")
    unidade = llm_output.get("unidade")

    final = build_output(nome, marca, cor, extras, quantidade, unidade)

    return final