import re

from .utils import clean_text, normalize_unit


# formata a unidade e quantidade com regra de singular/plural
def format_unit(qtd, unit):
    if not unit:
        return None

    unit = normalize_unit(unit)
    singular, plural = unit

    qtd = float(qtd)

    if qtd == 1:
        return f"{int(qtd)} {singular}"
    else:
        return f"{qtd:g} {plural}"


def postprocess(llm_output: str, medidas):
    text = clean_text(llm_output)

    text = re.sub(r"^\d+\.\s*", "", text)

    unidades_formatadas = [
        format_unit(qtd, unidade)
        for qtd, unidade in medidas
    ]

    unidades_formatadas = [u for u in unidades_formatadas if u]

    unidade_final = ", ".join(unidades_formatadas)

    return f"{text} - {unidade_final}"