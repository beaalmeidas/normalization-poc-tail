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


def postprocess(llm_output: str, quantidade, unidade):
    text = clean_text(llm_output)

    unidade_final = format_unit(quantidade, unidade)

    return f"{text} - {unidade_final}"