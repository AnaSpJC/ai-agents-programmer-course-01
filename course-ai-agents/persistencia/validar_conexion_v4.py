import os
import google.generativeai as genai
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI 

load_dotenv()

def validar():
    print("--- BLOQUE 2: FORZADO DE CANAL v1 (Nivel SDK) ---")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # 1. Configuramos el SDK de Google globalmente para usar v1
        # Esto debería sobreescribir cualquier intento de LlamaIndex de usar v1beta
        genai.configure(api_key=api_key, transport="grpc") 
        
        # 2. Instanciamos el modelo
        # Intentamos pasarle el cliente ya configurado si es posible, 
        # o al menos asegurar que la configuración global de 'genai' mande.
        llm = GoogleGenAI(
            model="models/gemini-1.5-flash", 
            api_key=api_key
        )
        
        # 3. Prueba de fuego
        # Si esto falla con 404 v1beta, significa que LlamaIndex 
        # tiene la URL 'v1beta' escrita en piedra en su código fuente.
        response = llm.complete("¿Qué versión de API estás usando?")
        
        print(f"✅ Conexión lograda: {response.text[:30]}")
        return True

    except Exception as e:
        print(f"❌ Error de nivel SDK: {e}")
        return False

if __name__ == "__main__":
    validar()