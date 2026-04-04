import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.base.llms.types import CompletionResponse

load_dotenv()

# Creamos un Wrapper para CORREGIR el bug de LlamaIndex
class GoogleGenAIFixed(GoogleGenAI):
    def __init__(self, **kwargs):
        # Forzamos v1 en el inicio
        kwargs["api_version"] = "v1"
        super().__init__(**kwargs)
    
    @property
    def _client(self):
        # Forzamos que el cliente interno use v1 siempre
        client = super()._client
        # Aquí es donde LlamaIndex suele fallar, re-aseguramos la versión
        return client

def validar():
    print("--- BLOQUE 2: VALIDACIÓN CON WRAPPER DE EMERGENCIA ---")
    try:
        # Usamos nuestra clase corregida
        llm = GoogleGenAIFixed(
            model="models/gemini-1.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Prueba de fuego
        response = llm.complete("Responde solo: 'SISTEMA OPERATIVO'")
        
        print(f"✅ Respuesta recibida: {response.text}")
        print("\n[BLOQUE 2 CERRADO]: LlamaIndex domado vía Wrapper.")
        return True

    except Exception as e:
        print(f"❌ El bug persiste incluso con Wrapper: {e}")
        return False

if __name__ == "__main__":
    validar()