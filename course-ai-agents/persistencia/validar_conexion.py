import os
from dotenv import load_dotenv
# Usamos la clase unificada que SIEMPRE usa la API v1 (estable)
from llama_index.llms.google_genai import Gemini 
from llama_index.core import Settings

load_dotenv()

def validar():
    print("--- BLOQUE 2: VALIDACIÓN DE CONECTOR UNIFICADO ---")
    try:
        # Instanciamos el modelo forzando la API estable
        llm = Gemini(
            model="models/gemini-1.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Prueba de fuego: ¿Nos responde Google sin error 404?
        response = llm.complete("¿Estás configurado en la versión estable v1?")
        
        print(f"✅ Conexión Exitosa.")
        print(f"🤖 Respuesta de Gemini: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Error de Conexión: {e}")
        return False

if __name__ == "__main__":
    validar()