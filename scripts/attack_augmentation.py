import pandas as pd
import random


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


df = pd.read_csv("./data/input/test.csv")

rows = []

for title in df["title"]:
    variations = augment(title)

    for var in variations:
        rows.append({
            "original": title,
            "attacked": var
        })

attack_df = pd.DataFrame(rows)
attack_df.to_csv("./data/input/attack.csv", index=False)

print("\n--- Dataset com attack augmentation 'attack.csv' gerado\n")