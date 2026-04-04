import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.google_genai import GooglePaLMEmbedding # Nombre alternativo por versión
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import chromadb

load_dotenv()

def run_diagnostic():
    print("=== INICIANDO DIAGNÓSTICO PROFESIONAL LLAMA-INDEX ===")
    
    try:
        # 1. Configurar el LLM (El que piensa)
        # Usamos 1.5-flash que es el caballo de batalla actual
        llm = Gemini(model="models/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        Settings.llm = llm
        print("✅ LLM Gemini configurado.")

        # 2. Configurar Embeddings (Tu modelo validado)
        embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001")
        Settings.embed_model = embed_model
        print("✅ Modelo de Embeddings validado.")

        # 3. Verificar persistencia de Chroma
        db_path = "./chroma_db"
        if os.path.exists(db_path):
            client = chromadb.PersistentClient(path=db_path)
            colls = client.list_collections()
            print(f"✅ ChromaDB encontrado. Colecciones actuales: {len(colls)}")
        else:
            print("⚠️ Advertencia: No se encontró la carpeta ./chroma_db en la raíz.")

        # 4. Prueba de fuego: Un razonamiento simple
        response = llm.complete("Hola, ¿estás listo para trabajar?")
        print(f"✅ Respuesta de Gemini: {response.text[:30]}...")
        
        print("\n[RESULTADO FINAL]: LUZ VERDE PARA LLAMA-INDEX")

    except Exception as e:
        print(f"\n❌ FALLO EN EL DIAGNÓSTICO: {type(e).__name__}")
        print(f"Detalle: {str(e)}")
        print("\n[RECOMENDACIÓN]: No avanzar hasta corregir este error.")

if __name__ == "__main__":
    run_diagnostic()