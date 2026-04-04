import os
from dotenv import load_dotenv
# CAMBIO CRÍTICO: El nombre de la clase es GoogleGenAI
from llama_index.llms.google_genai import GoogleGenAI 
from llama_index.core import Settings

load_dotenv()

def validar():
    print("--- BLOQUE 2: VALIDACIÓN DE CONECTOR UNIFICADO (v2) ---")
    try:
        # Instanciamos usando GoogleGenAI
        # Importante: No forzamos api_version aquí, la librería nueva 
        # ya sabe ir por el carril correcto (v1) por defecto.
        llm = GoogleGenAI(
            model="models/gemini-1.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Prueba de comunicación
        response = llm.complete("¿Conexión establecida?")
        
        print(f"✅ Conexión Exitosa.")
        print(f"🤖 Respuesta de Gemini: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Error de Conexión: {e}")
        return False

if __name__ == "__main__":
    validar()