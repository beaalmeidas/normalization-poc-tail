import pandas as pd
import random
import re

from src.utils import ensure_dir


# mapa para typos, teclas próximas no teclado
QWERTY_MAP = {
    "A": ["S", "Q", "Z"],
    "B": ["V", "G", "H", "N"],
    "C": ["X", "D", "F", "V"],
    "D": ["S", "E", "F", "C", "X"],
    "E": ["W", "R", "S", "D"],
    "F": ["D", "R", "G", "V", "C"],
    "G": ["F", "T", "H", "B", "V"],
    "H": ["G", "Y", "J", "N", "B"],
    "I": ["U", "O", "K", "J"],
    "J": ["H", "U", "K", "M", "N"],
    "K": ["J", "I", "L", "M"],
    "L": ["K", "O", "P"],
    "M": ["N", "J", "K"],
    "N": ["B", "H", "J", "M"],
    "O": ["I", "P", "L", "K"],
    "P": ["O", "L"],
    "Q": ["W", "A"],
    "R": ["E", "T", "F", "D"],
    "S": ["A", "W", "D", "Z", "X"],
    "T": ["R", "Y", "G", "F"],
    "U": ["Y", "I", "H", "J"],
    "V": ["C", "F", "G", "B"],
    "W": ["Q", "E", "S"],
    "X": ["Z", "S", "D", "C"],
    "Y": ["T", "U", "H"],
    "Z": ["A", "S", "X"]
}


def keyboard_typos(text, p=0.1):
    result = []

    # percorrendo cada caractere de cada item do dataset
    for char in text:
        upper = char.upper()

        # typo ocorre no caractere atual se o número sorteado
            # for menor que p = 10% de chance de typo
        if upper in QWERTY_MAP and random.random() < p:
            # escolhe uma tecla adjacente aleatória
            replacement = random.choice(QWERTY_MAP[upper])

            # if char.islower():
            #     replacement = replacement.lower()

            result.append(replacement)
        else:
            result.append(char)

    return "".join(result)


def random_separators(text):
    return (
        text
        .replace("-", " ")
        .replace("/", " ")
        .replace("  ", " ")
    )


def random_case(text):
    options = [
        text.lower(),
        text.upper(),
        text.capitalize()
    ]
    return random.choice(options)


def drop_words(text, p=0.2):
    words = text.split()
    words = [w for w in words if random.random() > p]
    return " ".join(words)


def shuffle_words(text):
    words = text.split()
    random.shuffle(words) 
    return " ".join(words)


# evitando que conjuntos semânticos "COM/SEM + substantivo" sejam separados
    # já que não seria uma alteração realista e atrapalharia o processamento
COMPOSITION_PATTERN = r"\b(SEM|COM)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ]+)"

def protect_compositions(text: str):
    protected = []

    def repl(match):
        token = f"__COMP_{len(protected)}__"
        protected.append(match.group(0))
        return token

    text = re.sub(COMPOSITION_PATTERN, repl, text)
    return text, protected


def restore_compositions(text: str, protected):
    for i, original in enumerate(protected):
        text = text.replace(f"__COMP_{i}__", original)
    return text


def augment(text):
    variations = [
        text,
        keyboard_typos(text),
        random_separators(text),
        random_case(text),
        drop_words(text),
        shuffle_words(text),
    ]

    return list(set([v for v in variations if v.strip()]))


ensure_dir("./data/input")

df = pd.read_csv("./data/input/test.csv")
df_benchmark = df.head(100)

rows = []

print(f"--- Gerando exatamente 6 variações para cada um dos {len(df_benchmark)} itens")

for title in df_benchmark["title"]:
    # Usamos um set para garantir que as variações sejam únicas
    variations = {title} # Começa com o título original
    
    # Enquanto não tivermos 6 variações únicas, continuamos tentando "atacar"
    attempts = 0
    while len(variations) < 6 and attempts < 50:
        # Aplica a função augment para gerar novas tentativas
        new_vars = augment(title)
        for v in new_vars:
            if len(variations) < 6:
                variations.add(v)
        attempts += 1

    # Adiciona as 6 variações ao dataset final
    for var in list(variations):
        rows.append({
            "original": title,
            "attacked": var
        })

attack_df = pd.DataFrame(rows)
attack_df.to_csv("./data/input/attack.csv", index=False)

print(f"\n--- Dataset 'attack.csv' gerado com {len(attack_df)} linhas.")
print(f"--- Verificação: {len(attack_df)/6} produtos originais processados.")