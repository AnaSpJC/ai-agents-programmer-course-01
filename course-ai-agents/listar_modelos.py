import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- LISTA DE MODELOS DISPONIBLES PARA TU LLAVE ---")
try:
    # Le pedimos a Google que nos diga qué modelos podemos usar
    for m in client.models.list():
        # Solo queremos los que permitan generar contenido
        if 'generateContent' in m.supported_methods:
            print(f"ID: {m.name} | Nombre: {m.display_name}")
except Exception as e:
    print(f"Error al listar: {e}")