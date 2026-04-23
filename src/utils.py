import re


def clean_text(text: str) -> str:
    text = text.upper()
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_number(text: str) -> str:
    return text.replace(",", ".")