import time
import random
from ollama import chat

from .config import MAX_RETRIES


def call_llm(prompt, max_retries=MAX_RETRIES):
    for attempt in range(MAX_RETRIES):
        try:
            response = chat(
                model='gemma2:latest',
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um sistema especializado em normalização de descrições de produtos de notas fiscais brasileiras."
                    },
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ],
                options={
                    "temperature": 0.0
                }
            )

            return response.message.content.strip()

        except Exception as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(f"\n--- Erro: {e}")
            print(f"\n--- Tentativa {attempt+1}/{max_retries} - aguardando {wait_time:.2f}s\n")

            time.sleep(wait_time)
