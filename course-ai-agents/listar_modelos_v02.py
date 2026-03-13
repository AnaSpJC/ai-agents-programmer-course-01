import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- BUSCANDO NOMBRES OFICIALES ---")
try:
    for m in client.models.list():
        # Imprimimos todo el objeto para ver cómo se llama la propiedad ahora
        print(f"ID: {m.name}")
except Exception as e:
    print(f"Error: {e}")