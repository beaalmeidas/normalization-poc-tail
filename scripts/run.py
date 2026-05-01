import pandas as pd
from google import genai
import os
from dotenv import load_dotenv
from src.pipeline import run_pipeline

load_dotenv()


API_KEY = os.getenv("API_KEY")
MODEL_ID = os.getenv("MODEL_ID")

client = genai.Client(api_key=API_KEY)


df = pd.read_csv("data/input/attack.csv")
df = df.sample(20, random_state=42)

df_few_shot = pd.read_csv("data/input/train_supervised.csv")

results = run_pipeline(
    data=df.to_dict(orient="records"),
    client=client,
    model_id=MODEL_ID,
    df_few_shot=df_few_shot
)

df_out = pd.DataFrame(results)
df_out.to_csv("data/output/normalized.csv", index=False)
print("\n--- Dataset final 'normalized.csv' gerado\n")