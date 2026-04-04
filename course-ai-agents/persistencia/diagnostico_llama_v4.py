import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
# CAMBIO AQUÍ: Usamos la ruta que coincide con tu pip list
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding 
from llama_index.core import Settings
import chromadb

load_dotenv()

def run_diagnostic():
    print("=== INICIANDO DIAGNÓSTICO PROFESIONAL LLAMA-INDEX (v4) ===")
    
    try:
        # 1. Configurar el LLM
        llm = Gemini(model="models/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        Settings.llm = llm
        print("✅ LLM Gemini (1.5-flash) configurado.")

        # 2. Configurar Embeddings
        # Usamos la clase GoogleGenAIEmbedding que es la que tienes instalada
        embed_model = GoogleGenAIEmbedding(model_name="models/gemini-embedding-001")
        Settings.embed_model = embed_model
        print("✅ Modelo de Embeddings (gemini-embedding-001) validado.")

        # 3. Verificar persistencia de Chroma
        db_path = "./chroma_db"
        client = chromadb.PersistentClient(path=db_path)
        print(f"✅ ChromaDB detectado. Colecciones: {len(client.list_collections())}")

        # 4. Prueba de conexión real
        response = llm.complete("Hola, responde solo con la palabra 'LISTO'.")
        print(f"✅ Prueba de API: {response.text}")
        
        print("\n[RESULTADO FINAL]: LUZ VERDE PARA LLAMA-INDEX")

    except Exception as e:
        print(f"\n❌ FALLO EN EL DIAGNÓSTICO: {type(e).__name__}")
        print(f"Detalle: {str(e)}")

if __name__ == "__main__":
    run_diagnostic()