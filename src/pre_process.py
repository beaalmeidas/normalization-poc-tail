import re

from .utils import clean_text, normalize_number


# extrai informações de medidas e embalagem dos dados crus
    # retorna um dicionário com cada ponto definido
    # caso algum não seja aplicável, retorna none
def extract_measurement_and_packaging(text: str):
    number = r"(\d+(?:[.,]\d+)?)"
    units = r"(ML|L|LT|LTS|G|GR|KG|QUILO|KILO|MM|CM|M|UN|UND|CX|PCT|FD|DZ|KB|MB|GB|TB)"

    peso_volume = re.search(rf"{number}\s*{units}", text)
    dimensao = re.search(rf"{number}\s*(MM|CM|M|GB|TB|MB|KB)", text)
    tipo_embalagem = re.search(r"(CX|PCT|FD|DZ)\s*(?:C\/\s*)?(\d+)", text)
    unidade_simples = re.search(r"(\d+)\s*(UN|UND)", text)
    multipack = re.search(rf"(\d+)\s*[xX]\s*{number}\s*{units}", text)

    return {
        "peso_volume": peso_volume.groups() if peso_volume else None,
        "tipo_embalagem": tipo_embalagem.groups() if tipo_embalagem else None,
        "unidade_simples": unidade_simples.groups() if unidade_simples else None,
        "dimensao": dimensao.groups() if dimensao else None,
        "multipack": multipack.groups() if multipack else None,
    }


# realiza conversões entre unidades em casos de produtos iguais
    # com unidades diferentes
def convert_to_base_unit(valor: float, unidade: str):
    unidade = unidade.upper()

    conversion_map = {
        "L": ("ML", 1000),
        "LT": ("ML", 1000),
        "LTS": ("ML", 1000),
        "ML": ("ML", 1),

        "KG": ("G", 1000),
        "QUILO": ("G", 1000),
        "KILO": ("G", 1000),
        "G": ("G", 1),
        "GR": ("G", 1),
    }

    if unidade in conversion_map:
        base_unit, factor = conversion_map[unidade]
        return valor * factor, base_unit

    return valor, unidade


# define quantidades e embalagem em pares número-unidade
def parse_measurements_and_packaging(medidas: dict):
    result = []

    if medidas["peso_volume"]:
        valor, unidade = medidas["peso_volume"]
        valor = float(valor.replace(",", "."))

        valor_convertido, unidade_convertida = convert_to_base_unit(valor, unidade)
        valor_convertido = round(valor_convertido, 2)

        result.append((valor_convertido, unidade_convertida))

    if medidas["tipo_embalagem"]:
        tipo, qtd = medidas["tipo_embalagem"]
        result.append((int(qtd), tipo))

    if medidas["unidade_simples"]:
        qtd, unidade = medidas["unidade_simples"]
        result.append((int(qtd), unidade))

    if medidas["multipack"]:
        qtd_pack, valor, unidade = medidas["multipack"]

        valor = float(valor.replace(",", "."))
        qtd_pack = int(qtd_pack)

        valor_convertido, unidade_convertida = convert_to_base_unit(valor, unidade)

        total = qtd_pack * valor_convertido
        total = round(total, 2)

        result.append((total, unidade_convertida))

    return result if result else [(1, "UN")]


def preprocess(text: str) -> dict:
    text = clean_text(text)
    text = normalize_number(text)

    medidas = extract_measurement_and_packaging(text)

    medidas_formatadas = parse_measurements_and_packaging(medidas)

    return {
        "raw": text,
        "medidas": medidas_formatadas
    }
