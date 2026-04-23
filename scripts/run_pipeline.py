import pandas as pd
from google import genai
import os
from dotenv import load_dotenv
from src.pipeline import run_pipeline

load_dotenv()


API_KEY = os.getenv("API_KEY")
MODEL_ID = os.getenv("MODEL_ID")

client = genai.Client(api_key=API_KEY)

df = pd.read_csv("data/test.csv")

results = run_pipeline(
    data=df["descricao"].tolist(),
    client=client,
    model_id=MODEL_ID
)

df["normalizado"] = [r["output"] for r in results]
df.to_csv("data/results.csv", index=False)