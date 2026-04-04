import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("--- PROTOCOLO DE DIAGNÓSTICO: MODELOS DISPONIBLES ---")
try:
    for m in genai.list_models():
        # Filtramos los que permiten generar contenido y crear embeddings
        methods = ", ".join(m.supported_generation_methods)
        print(f"ID: {m.name} | Métodos: {methods}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")