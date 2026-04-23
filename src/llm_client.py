import time


def call_llm(client, model_id, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config={"temperature": 0.0}
            )

            return response.text.strip()

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(1)

    return None