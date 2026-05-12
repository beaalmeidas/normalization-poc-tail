
import pandas as pd
from google import genai
import os
from dotenv import load_dotenv

from src.pipeline import run_pipeline
from src.utils import ensure_dir

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL_ID = os.getenv("MODEL_ID")

client = genai.Client(api_key=API_KEY)

# --- Carrega os dados ---
df_attack    = pd.read_csv("data/input/attack.csv")
df_normalized = pd.read_csv("data/output/normalized.csv")
df_few_shot  = pd.read_csv("data/input/train_supervised.csv")

print(f"Total no attack.csv:     {len(df_attack)}")
print(f"Total no normalized.csv: {len(df_normalized)}")

# --- Identifica os itens faltando pelo campo 'attacked' ---
attacked_ok = set(df_normalized["attacked"].str.strip())
df_missing = df_attack[~df_attack["attacked"].str.strip().isin(attacked_ok)]

print(f"Itens faltando:          {len(df_missing)}")

if df_missing.empty:
    print("\n--- Nenhum item faltando! O CSV já está completo.")
    exit(0)

print(f"\nRodando pipeline para os {len(df_missing)} itens faltando...\n")

# --- Roda o pipeline só nos faltantes ---
results = run_pipeline(
    data=df_missing.to_dict(orient="records"),
    client=client,
    model_id=MODEL_ID,
    df_few_shot=df_few_shot,
)

if not results:
    print("\n--- Pipeline não retornou resultados. Verifique os erros acima.")
    exit(1)

# --- Concatena e salva sobrescrevendo o normalized.csv ---
df_new   = pd.DataFrame(results)
df_final = pd.concat([df_normalized, df_new], ignore_index=True)

ensure_dir("data/output")
df_final.to_csv("data/output/normalized.csv", index=False)

print(f"\n--- normalized.csv atualizado: {len(df_final)} linhas ({len(df_new)} novas adicionadas)")