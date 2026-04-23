import time


def call_llm(client, prompt: str, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception:
            time.sleep(1)
    return None