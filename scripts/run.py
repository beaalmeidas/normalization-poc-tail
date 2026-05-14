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


df = pd.read_csv("data/input/attack.csv")
#df = df.sample(10, random_state=42)

df_few_shot = pd.read_csv("data/input/train_supervised.csv")

results = run_pipeline(
    data=df.to_dict(orient="records"),
    client=client,
    model_id=MODEL_ID,
    df_few_shot=df_few_shot
)

if not results:
    print("\n--- Nenhum resultado gerado. Pipeline falhou ou LLM não retornou dados válidos.\n")
    exit(1)

ensure_dir("./data/output")

df_out = pd.DataFrame(results)
df_out.to_csv("data/output/normalized.csv", index=False)
print("\n--- Dataset final 'normalized.csv' gerado\n")