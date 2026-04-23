import pandas as pd
import random


def shuffle_words(text):
    words = text.split()
    random.shuffle(words)
    return " ".join(words)

def remove_spaces(text):
    return text.replace(" ", "")

def add_noise(text):
    return text.replace("O", "0").replace("A", "@")

def augment(text):
    return list(set([
        text,
        shuffle_words(text),
        remove_spaces(text),
        add_noise(text),
    ]))

df = pd.read_csv("data/test.csv")

rows = []

for title in df["title"]:
    variations = augment(title)

    for var in variations:
        rows.append({
            "original": title,
            "attacked": var
        })

attack_df = pd.DataFrame(rows)
attack_df.to_csv("data/attack.csv", index=False)

print("\n--- Dataset attack.csv gerado\n")