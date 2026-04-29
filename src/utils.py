import re


# padroniza o texto para maiúsculo, remove espaços duplos ou no início e fim
def clean_text(text: str) -> str:
    text = text.upper()
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


# padroniza decimais para usarem ponto
def normalize_number(text: str) -> str:
    return text.replace(",", ".")