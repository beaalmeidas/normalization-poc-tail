import time
import random

from .config import MAX_RETRIES


def call_llm(client, model_id, prompt, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config={"temperature": 0.0}
            )

            return response.text.strip()

        except Exception as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(f"Erro: {e}")
            print(f"Tentativa {attempt+1}/{max_retries} → aguardando {wait_time:.2f}s\n")

            time.sleep(wait_time)

    print("\n--- Falhou após retries\n")
    return None