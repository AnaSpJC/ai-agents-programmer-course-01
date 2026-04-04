import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
import chromadb

load_dotenv()

def run_diagnostic():
    print("=== INICIANDO DIAGNÓSTICO PROFESIONAL LLAMA-INDEX (v3) ===")
    
    try:
        # 1. Configurar el LLM (El que piensa)
        # Usamos 1.5-flash
        llm = Gemini(model="models/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        Settings.llm = llm
        print("✅ LLM Gemini configurado.")

        # 2. Configurar Embeddings (Tu modelo validado)
        # Cambiamos a la clase estándar que tu sistema reconoció
        embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001")
        Settings.embed_model = embed_model
        print("✅ Modelo de Embeddings validado.")

        # 3. Verificar persistencia de Chroma
        db_path = "./chroma_db"
        client = chromadb.PersistentClient(path=db_path)
        colls = client.list_collections()
        print(f"✅ ChromaDB encontrado. Colecciones actuales: {len(colls)}")

        # 4. Prueba de fuego: Un razonamiento simple
        response = llm.complete("Hola, ¿estás listo para trabajar?")
        print(f"✅ Respuesta de Gemini: {response.text[:30]}...")
        
        print("\n[RESULTADO FINAL]: LUZ VERDE PARA LLAMA-INDEX")

    except Exception as e:
        print(f"\n❌ FALLO EN EL DIAGNÓSTICO: {type(e).__name__}")
        print(f"Detalle: {str(e)}")
        print("\n[RECOMENDACIÓN]: Verifica que la carpeta ./chroma_db exista en /persistencia.")

if __name__ == "__main__":
    run_diagnostic()