import json
import pandas as pd
import re

from sklearn.model_selection import train_test_split

from src.utils import ensure_dir


# extraindo dados dos datasets octaprice
def extract_title_from_url(url: str) -> str:
    match = re.search(r"MLB-\d+-(.+)", url)
    if not match:
        return None

    slug = match.group(1)

    slug = re.sub(r"_JM$", "", slug)

    return (
        slug.replace("-", " ")
            .replace("_", " ")
            .strip()
            .lower()
    )


with open("./data/initial/octaprice_mercadolivre_1.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)

df1 = pd.DataFrame(data1)
df1["title"] = df1["product_url"].apply(extract_title_from_url)
df1 = df1[["title"]]


with open("./data/initial/octaprice_mercadolivre_2.json", "r", encoding="utf-8") as f:
    data2 = json.load(f)

df2 = pd.DataFrame(data2)
df2["title"] = df2["product_url"].apply(extract_title_from_url)
df2 = df2[["title"]]


df_final = pd.concat([df1, df2], ignore_index=True)


# padronizando e limpando dataset não-supervisionado
df_final["title"] = df_final["title"].str.upper().str.strip()

df_final = (
    df_final
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

ensure_dir("./data/input")

df_final.to_csv("./data/input/test.csv", index=False, encoding="utf-8")
print("\n--- Dataset inicial 'test.csv' gerado\n")


# dividindo dataset supervisionado em conjuntos de treino e teste
df_initial = pd.read_csv("./data/initial/itens_nf_normalizados.csv")

train, test = train_test_split(df_initial, test_size=0.2, random_state=42)

train.to_csv("./data/input/train_supervised.csv", index=False, encoding="utf-8")
print("\n--- Dataset de treino 'train_supervised.csv' gerado\n")

test.to_csv("./data/input/test_supervised.csv", index=False, encoding="utf-8")
print("\n--- Dataset de teste 'test_supervised.csv' gerado\n")