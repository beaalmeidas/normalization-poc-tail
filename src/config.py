TEMPLATE = "{nome} {marca} {cor} {extras} - {quantidade} {unidade}"

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

BATCH_SIZE = 10
MAX_RETRIES = 3