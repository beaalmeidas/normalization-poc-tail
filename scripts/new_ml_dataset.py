import json
import pandas as pd
import re


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


# padronizando e limpando
df_final["title"] = df_final["title"].str.upper().str.strip()

df_final = (
    df_final
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

df_final.to_csv("./data/input/test.csv", index=False, encoding="utf-8")