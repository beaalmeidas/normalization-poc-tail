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
            error_str = str(e)
            is_overload = "503" in error_str or "UNAVAILABLE" in error_str or "overloaded" in error_str.lower()

            if is_overload:
                # Sobrecarga: espera curta fixa com jitter
                wait_time = 10 + random.uniform(0, 5)
            else:
                # Outros erros: backoff moderado, máximo 60s
                wait_time = min(2 ** attempt + random.uniform(0, 3), 60)

            print(f"Erro: {e}")
            print(f"Tentativa {attempt+1}/{max_retries} → aguardando {wait_time:.2f}s\n")
            time.sleep(wait_time)

    print("\n--- Falhou após retries\n")
    return None
