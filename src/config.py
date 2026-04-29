TEMPLATE = "{nome} {marca} {extras} - {quantidade} {unidade}"

UNITS_MAP = {
    # Peso / volume
    "ML": ("MILILITRO", "MILILITROS"),
    "L": ("LITRO", "LITROS"),
    "LT": ("LITRO", "LITROS"),
    "LTS": ("LITRO", "LITROS"),

    "G": ("GRAMA", "GRAMAS"),
    "GR": ("GRAMA", "GRAMAS"),
    "KG": ("QUILOGRAMA", "QUILOGRAMAS"),
    "QUILO": ("QUILOGRAMA", "QUILOGRAMAS"),
    "KILO": ("QUILOGRAMA", "QUILOGRAMAS"),

    # Dimensão
    "MM": ("MILÍMETRO", "MILÍMETROS"),
    "CM": ("CENTÍMETRO", "CENTÍMETROS"),
    "M": ("METRO", "METROS"),

    # Unidade comercial
    "UN": ("UNIDADE", "UNIDADES"),
    "UND": ("UNIDADE", "UNIDADES"),
    "CX": ("CAIXA", "CAIXAS"),
    "PCT": ("PACOTE", "PACOTES"),
    "FD": ("FARDO", "FARDOS"),
    "DZ": ("DÚZIA", "DÚZIAS"),
}

BATCH_SIZE = 10
MAX_RETRIES = 3