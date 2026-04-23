import re
from .utils import clean_text, normalize_number


def extract_measure(text: str):
    match = re.search(r"(\d+(?:\.\d+)?)\s*(ML|L|G|KG)", text)
    if match:
        return match.group(1), match.group(2)
    return None, None

def preprocess(text: str) -> dict:
    text = clean_text(text)
    text = normalize_number(text)

    quantidade, unidade = extract_measure(text)

    return {
        "raw": text,
        "quantidade": quantidade,
        "unidade": unidade
    }