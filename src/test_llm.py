# from google import genai
# from pathlib import Path
import os
from ollama import chat
from dotenv import load_dotenv

load_dotenv()


model_id = os.getenv("MODEL_ID")

response = chat(
    model=model_id,
    messages=[{'role': 'user', 'content': 'Hello! Are you working?'}],
)
print(response.message.content)