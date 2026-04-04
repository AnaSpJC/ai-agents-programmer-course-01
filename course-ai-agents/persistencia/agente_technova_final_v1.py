import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. CONFIGURACIÓN DE MODELOS (Tu fórmula ganadora)
Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)

lc_embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=api_key
)
Settings.embed_model = LangchainEmbedding(lc_embed_model)

def ejecutar_persistencia_vectorial():
    print("--- 💾 FASE 1: CIERRE CON PERSISTENCIA EN CHROMADB ---")
    
    # 2. CONFIGURAR EL ALMACENAMIENTO (ChromaDB)
    # Esto apunta a la carpeta que ya tenés en tu árbol de archivos
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("manual_technova")
    
    # Definimos el contenedor para LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    try:
        # 3. LÓGICA DE CARGA INTELIGENTE
        # Si la carpeta tiene datos, los usamos. Si no, leemos el archivo.
        if chroma_collection.count() > 0:
            print("✅ Datos encontrados en ChromaDB. Cargando desde el disco...")
            index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )
        else:
            print("📖 No hay datos previos. Leyendo 'mi_empresa.txt' e indexando...")
            documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )
            print("💾 ¡Manual guardado en ChromaDB exitosamente!")

        # 4. CONSULTA
        query_engine = index.as_query_engine()
        pregunta = "¿Cuál es el código de autorización para reembolsos?"
        respuesta = query_engine.query(pregunta)
        
        print(f"\n🤖 IA (Basado en DB): {respuesta}")

    except Exception as e:
        print(f"❌ Error en la persistencia: {e}")

if __name__ == "__main__":
    ejecutar_persistencia_vectorial()