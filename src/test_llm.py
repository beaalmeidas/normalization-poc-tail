from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path


def main():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    model_id = os.getenv("MODEL_ID")

    if not model_id:
        print("\n--- Id da LLM não encontrado na .env\n")
        return

    client = genai.Client()

    print("\n")
    response = client.models.generate_content(
        model=model_id,
        contents="Responda apenas: Sou a LLM e estou funcionando!"
    )
    print("\n")

    try:
        print(response.text)
    except:
        try:
            print(response.candidates[0].content.parts[0].text)
        except Exception as e:
            print("\n--- Erro ao ler resposta:", e)
            print(response)


if __name__ == "__main__":
    main()