import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI 

load_dotenv()

def validar():
    print("--- BLOQUE 2: CIERRE DE CONEXIÓN ESTABLE ---")
    try:
        # EL CAMBIO DEFINITIVO: Forzamos api_version="v1"
        llm = GoogleGenAI(
            model="models/gemini-1.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY"),
            api_version="v1"  # <--- Esta es la llave que abre la puerta
        )
        
        # Prueba de comunicación
        response = llm.complete("Responde solo: CONEXIÓN EXITOSA V1")
        
        print(f"✅ {response.text}")
        return True
    except Exception as e:
        print(f"❌ Error persistente: {e}")
        return False

if __name__ == "__main__":
    validar()