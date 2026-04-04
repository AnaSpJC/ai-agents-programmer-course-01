import os
from dotenv import load_dotenv
# Importamos la clase que usa INTERNAMENTE el 'genai.Client' que pusiste arriba
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

load_dotenv()

def validar():
    print("--- BLOQUE 2: CONEXIÓN POR SDK UNIFICADO (Sincronizada) ---")
    try:
        api_key = os.getenv("GEMINI_API_KEY") # Usamos tu variable original
        
        # Configuramos el LLM igual que en tu script inicial:
        # 1. Sin el prefijo 'models/'
        # 2. Dejando que la librería elija la versión (v1) por defecto
        llm = GoogleGenAI(
            model="gemini-2.5-flash", # El modelo que te funcionó
            api_key=api_key
        )
        
        # Prueba de fuego
        response = llm.complete("Hola, ¿me recibís por el canal nuevo?")
        
        print(f"✅ RESPUESTA: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    validar()