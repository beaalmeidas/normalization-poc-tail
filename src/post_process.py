import re
from .config import UNITS_MAP
from .utils import clean_text


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

def postprocess(llm_output: str, quantidade, unidade):
    text = llm_output.clean_text()

    singular, plural = UNITS_MAP.get(unidade.upper(), (unidade, unidade))

    quantidade = float(quantidade)

    if quantidade == 1:
        unidade_final = singular
    else:
        unidade_final = plural

    return f"{text} - {quantidade:g} {unidade_final}"