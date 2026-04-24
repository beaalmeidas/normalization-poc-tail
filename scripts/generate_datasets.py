import pandas as pd
import re

UNITS_MAP = {
    "ML": ("MILILITRO", "MILILITROS"),
    "L": ("LITRO", "LITROS"),
    "LT": ("LITRO", "LITROS"),
    "LTS": ("LITRO", "LITROS"),
    "LITRO": ("LITRO", "LITROS"),
    "LITROS": ("LITRO", "LITROS"),

    "G": ("GRAMA", "GRAMAS"),
    "GR": ("GRAMA", "GRAMAS"),
    "GRAMAS": ("GRAMA", "GRAMAS"),

    "KG": ("QUILOGRAMA", "QUILOGRAMAS"),
    "QUILOGRAMA": ("QUILOGRAMA", "QUILOGRAMAS"),
    "QUILOGRAMAS": ("QUILOGRAMA", "QUILOGRAMAS"),
}


def normalize_text(text: str):
    text = text.upper()

    text = (
        text.replace("Á", "A")
        .replace("Ã", "A")
        .replace("Â", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace("Ç", "C")
    )

    return text


def resolve_unit(unit, quantidade):
    if not unit:
        return "UNIDADE"

    unit = unit.upper()

    singular, plural = UNITS_MAP.get(unit, (unit, unit))

    try:
        qtd = float(quantidade)
    except:
        return plural

    if qtd == 1:
        return singular
    else:
        return plural


def extract_measure(text: str):
    pattern = r"(\d+(?:\.\d+)?)\s*(LITROS?|ML|LTS|LT|L|QUILOGRAMAS?|KG|GRAMAS?|GR|G)"
    match = re.search(pattern, text)

    if match:
        qtd = match.group(1)
        unit = match.group(2).upper()

        unit_norm = UNITS_MAP.get(unit, unit)

        return qtd, unit

    return None, None


def remove_measure(text: str):
    return re.sub(
        r"(\d+(?:\.\d+)?)\s*(LITROS?|ML|LTS|LT|L|QUILOGRAMAS?|KG|GRAMAS?|GR|G)",
        "",
        text
    )


def normalize_output(text: str):
    text = normalize_text(text)

    qtd, unidade = extract_measure(text)

    if not qtd:
        qtd = "1"
        unidade = "UNIDADE"

    nome_parte = remove_measure(text)
    nome_parte = re.sub(r"\s+", " ", nome_parte).strip()

    # remove hífen duplicado
    nome_parte = nome_parte.replace("-", " ")

    # monta final
    final = f"{nome_parte} {DEFAULT_COLOR} - {qtd} {unidade}"

    return final.strip()


def main():
    df = pd.read_csv("data/itens_nf_normalizacao.csv")

    # =========================
    # FEW-SHOT (treino)
    # =========================
    df["item_normalizado"] = df["item_normalizado"].apply(normalize_output)

    df_few_shot = df[["item_nao_normalizado", "item_normalizado"]]

    df_few_shot.to_csv("data/few_shot.csv", index=False)

    print("--- few_shot.csv gerado")

    # =========================
    # TEST (entrada para attack)
    # =========================
    df_test = df[["item_nao_normalizado"]].copy()
    df_test.columns = ["title"]

    df_test.to_csv("data/test.csv", index=False)

    print("--- test.csv gerado")


if __name__ == "__main__":
    main()