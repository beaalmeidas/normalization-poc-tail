import re
from .config import TEMPLATE, UNITS_MAP, DEFAULT_COLOR


def normalize_unit(unit: str):
    if not unit:
        return None
    return UNITS_MAP.get(unit.upper(), unit)

def ensure_color(text: str):
    if " S/C " in text:
        return text

    if " - " in text:
        left, right = text.split(" - ")
        if len(left.split()) < 3:
            left += " S/C"
        return f"{left} - {right}"

    return text

def fix_unit(text: str):
    pattern = r"(\d+(?:\.\d+)?)\s*(ML|L|KG|G|UN|UND|CX|PCT|DZ)"
    
    def repl(match):
        qtd = match.group(1)
        unit = normalize_unit(match.group(2))
        return f"{qtd} {unit}"

    return re.sub(pattern, repl, text)

def postprocess(text: str):
    text = text.upper()
    text = fix_unit(text)
    text = ensure_color(text)

    return text