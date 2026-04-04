import os
import google.generativeai as genai
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

def validar():
    print("--- BLOQUE 2: INYECCIÓN DE CLIENTE v1 ---")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # 1. Creamos el modelo usando el SDK de Google DIRECTAMENTE
        # El SDK de Google sí respeta la jerarquía de modelos en v1
        google_client = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # 2. Configuramos LlamaIndex pasándole el cliente ya existente
        # Al pasarle 'client', LlamaIndex debería usar esta instancia 
        # en lugar de intentar crear una nueva con v1beta
        llm = GoogleGenAI(
            model="models/gemini-1.5-flash",
            api_key=api_key
        )
        
        # 3. FORZADO MANUAL DEL CLIENTE INTERNO
        # Esta es la 'cirugía mayor': le cambiamos el cliente por la fuerza
        from google.ai.generativelanguage_v1 import ModelServiceClient
        llm._client = ModelServiceClient(client_options={"api_key": api_key})
        
        # Prueba de fuego
        response = llm.complete("¿Estamos en v1?")
        
        print(f"✅ RESPUESTA: {response.text}")
        print("\n[BLOQUE 2 CERRADO]: LlamaIndex forzado exitosamente.")
        return True

    except Exception as e:
        print(f"❌ Error crítico de inyección: {e}")
        return False

if __name__ == "__main__":
    validar()