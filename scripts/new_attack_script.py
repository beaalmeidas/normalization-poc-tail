import os
import re
import json
import time
import logging
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ── Configuração ───────────────────────────────────────────────
INPUT_PATH   = "data/input/test.csv"
INPUT_COLUMN = "title"
ATTACK_PATH  = "data/input/attack.csv"

RANDOM_SEED  = 42
BATCH_SIZE   = 5
API_KEY      = os.getenv("API_KEY")
ATTACK_MODEL = os.getenv("ATTACK_MODEL_ID", "gemini-2.5-flash-preview-05-20")

ATTACK_PROMPT = """
Você é um gerador de variantes adversariais de títulos de produtos de e-commerce brasileiro.

TAREFA
Para cada título recebido (identificado por idx), gere 6 (SEIS) variantes adversariais, distribuídas em 3 estratégias diferentes.
Retorne SOMENTE um array JSON. Sem texto extra, sem markdown.

O formato OBRIGATÓRIO do JSON para CADA objeto no array deve ser:
{
    "idx": int,
    "attacks": [
        {"tipo": "Abreviacao", "texto": "var1"},
        {"tipo": "Abreviacao", "texto": "var2"},
        {"tipo": "Notacao_Unidades", "texto": "var3"},
        {"tipo": "Notacao_Unidades", "texto": "var4"},
        {"tipo": "Erro_Digitacao", "texto": "var5"},
        {"tipo": "Erro_Digitacao", "texto": "var6"}
    ]
}

ESTRATÉGIAS OBRIGATÓRIAS (Faça exatamente 2 variantes diferentes para cada tipo):
    1. "Abreviacao": Abreviar palavras longas (ex: "Liquidificador" → "Liq.")
    2. "Notacao_Unidades": Notação alternativa de unidades (ex: "500ml" → "0,5L", "12kg" → "12 kilos")
    3. "Erro_Digitacao": Erro de digitação / Trocar caracteres adjacentes (ex: "Samsung" → "Samsugn")
"""


def attack_batch_llm(
    titles: list[str],
    client: genai.Client,
    start_idx: int = 0,
) -> list[dict]:
    lines = [f'[{start_idx + i}] "{t}"' for i, t in enumerate(titles)]
    user_prompt = "\n".join(lines)

    try:
        response = client.models.generate_content(
            model=ATTACK_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=ATTACK_PROMPT,
                temperature=0.7,
                max_output_tokens=2048,
                response_mime_type="application/json",
            ),
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?", "", raw_text).rstrip("`").strip()
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            parsed = [parsed]
        return parsed

    except json.JSONDecodeError:
        matches = re.findall(r"\{[^{}]+\}", raw_text, re.DOTALL)
        results = []
        for m in matches:
            try:
                results.append(json.loads(m))
            except json.JSONDecodeError:
                continue
        return results or [{"idx": start_idx + i, "attacked": t} for i, t in enumerate(titles)]

    except Exception as e:
        logger.error("Erro attack LLM: %s", e)
        return [{"idx": start_idx + i, "attacked": t} for i, t in enumerate(titles)]


def run_attack(
    input_path=INPUT_PATH,
    input_column=INPUT_COLUMN,
    attack_path=ATTACK_PATH,
    n_sample=100,
):
    client = genai.Client(api_key=API_KEY)

    df = pd.read_csv(input_path)
    df_sample = df[[input_column]].sample(n=n_sample, random_state=RANDOM_SEED).reset_index(drop=True)
    print(f"Títulos para processar: {len(df_sample)}")

    titles_orig = df_sample[input_column].tolist()
    n_attack = len(titles_orig)
    registros_ataque = []

    for batch_start in tqdm(range(0, n_attack, BATCH_SIZE), desc="Attack", unit="batch"):
        batch_end = min(batch_start + BATCH_SIZE, n_attack)
        batch = titles_orig[batch_start:batch_end]

        raw_list = attack_batch_llm(batch, client, start_idx=batch_start)

        for local_i in range(batch_end - batch_start):
            global_i = batch_start + local_i

            matched = next(
                (r for r in raw_list if isinstance(r, dict) and r.get("idx") == global_i),
                None,
            )

            if matched and "attacks" in matched and isinstance(matched["attacks"], list):
                ataques = matched["attacks"]
            else:
                ataques = [{"tipo": "Fallback_Erro_LLM", "texto": titles_orig[global_i]}] * 6

            for ataque in ataques:
                if isinstance(ataque, dict):
                    tipo  = ataque.get("tipo", "Desconhecido")
                    texto = ataque.get("texto", titles_orig[global_i])
                else:
                    tipo  = "Desconhecido"
                    texto = str(ataque)

                registros_ataque.append({
                    "id": global_i,
                    "original": titles_orig[global_i],
                    "tipo_variacao": tipo,
                    "attacked": texto,
                })

        time.sleep(2)

    df_attack = pd.DataFrame(registros_ataque)
    os.makedirs(os.path.dirname(attack_path), exist_ok=True)
    df_attack.to_csv(attack_path, index=False, encoding="utf-8-sig")
    print(f"\n--- Attack concluído: {len(titles_orig)} títulos → {len(df_attack)} linhas → {attack_path}")
    return df_attack


if __name__ == "__main__":
    run_attack()
