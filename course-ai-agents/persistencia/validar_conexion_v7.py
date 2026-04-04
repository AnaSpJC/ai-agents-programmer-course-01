import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

load_dotenv()

def validar():
    print("--- BLOQUE 2: VALIDACIÓN CON SDK UNIFICADO (v7) ---")
    try:
        # En la versión nueva, NO usamos el prefijo 'models/' 
        # y la librería ya apunta a v1 por defecto.
        llm = GoogleGenAI(
            model="gemini-1.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        response = llm.complete("¿Estás operando con el nuevo SDK google-genai?")
        
        print(f"✅ ÉXITO TOTAL: {response.text[:50]}")
        return True
    except Exception as e:
        print(f"❌ Error final: {e}")
        return False

if __name__ == "__main__":
    validar()