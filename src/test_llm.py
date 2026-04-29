from pathlib import Path

from google import genai
import os
from dotenv import load_dotenv


def main():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    model_id = os.getenv("MODEL_ID")

    if not model_id:
        print("MODEL_ID não encontrado na .env")
        return

    client = genai.Client()

    response = client.models.generate_content(
        model=model_id,
        contents="Responda apenas: OK"
    )

    try:
        print(response.text)
    except:
        try:
            print(response.candidates[0].content.parts[0].text)
        except Exception as e:
            print("Erro ao ler resposta:", e)
            print(response)


if __name__ == "__main__":
    main()