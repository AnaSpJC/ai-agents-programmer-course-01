import os
from dotenv import load_dotenv
# El LLM sigue siendo de LlamaIndex (porque el 2.5 te funcionó ahí)
from llama_index.llms.google_genai import GoogleGenAI
# Usamos el puente de LangChain para los Embeddings (porque LangChain NO falla en la ruta)
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. LLM: Tu configuración ganadora
Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)

# 2. EMBEDDINGS: El bypass definitivo
# Usamos LangChain para crear el vector porque LangChain usa la API v1 (estable)
lc_embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",  # Modelo correcto para embeddings
    google_api_key=api_key
)
# Se lo entregamos a LlamaIndex envuelto en su adaptador
Settings.embed_model = LangchainEmbedding(lc_embed_model)

def iniciar():
    print("--- BLOQUE 3: RAG HÍBRIDO (Bypass de Embeddings) ---")
    try:
        print("📖 Cargando manual...")
        documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()

        print("🧠 Indexando con motor LangChain (v1 estable)...")
        # Ahora LlamaIndex usará el motor de LangChain que no da error 404
        index = VectorStoreIndex.from_documents(documents)

        print("🔍 Consultando al manual...")
        query_engine = index.as_query_engine()
        respuesta = query_engine.query("¿Cuál es el código de autorización para reembolsos?")
        
        print("\n" + "="*50)
        print(f"IA (Technova): {respuesta}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    iniciar()