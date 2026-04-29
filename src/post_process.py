import re
from .config import TEMPLATE, UNITS_MAP


def normalize_unit(unit: str):
    if not unit:
        return None
    return UNITS_MAP.get(unit.upper(), unit)

# def fix_unit(text: str):
#     pattern = r"(\d+(?:\.\d+)?)\s*(ML|L|KG|G|UN|UND|CX|PCT|DZ)"
    
#     def repl(match):
#         qtd = match.group(1)
#         unit = normalize_unit(match.group(2))
#         return f"{qtd} {unit}"

#     return re.sub(pattern, repl, text)

def format_unit(qtd, unit):
    if not unit:
        return None

    unit = unit.upper()
    singular, plural = UNITS_MAP.get(unit, (unit, unit))

    qtd = float(qtd)

    if qtd == 1:
        return f"{int(qtd)} {singular}"
    else:
        return f"{qtd:g} {plural}"

def postprocess(text: str):
    # text = text.upper()
    # text = fix_unit(text)

    # return text
    text = text.upper()

    unidade_final = apply_unit_rules(text)

    # Remove unidades antigas do texto (opcional, melhora qualidade)
    text = re.sub(r"\d+(?:\.\d+)?\s*(ML|L|LT|G|KG|CX|PCT|FD|DZ|UN|UND)", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return f"{text} - {unidade_final}"