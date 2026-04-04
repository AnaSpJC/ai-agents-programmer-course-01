import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

load_dotenv()
# Usamos la variable que definiste en tu script exitoso
api_key = os.getenv("GEMINI_API_KEY")

# CONFIGURACIÓN TÉCNICA DEFINITIVA
# Usamos 1.5-flash: es estable, tiene cuota y YA FUNCIONA con el conector nuevo.
Settings.llm = GoogleGenAI(
    model="gemini-1.5-flash", 
    api_key=api_key
)

# Para los embeddings (vectores), usamos el modelo estándar de Google
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/text-embedding-004", 
    api_key=api_key
)

def ejecutar_rag():
    print("--- BLOQUE 3: RAG CON VERSIÓN ESTABLE ---")
    try:
        # Carga del manual (un nivel arriba de /persistencia)
        documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()

        # Creación del índice
        print("Transformando texto en vectores...")
        index = VectorStoreIndex.from_documents(documents)

        # Consulta
        query_engine = index.as_query_engine()
        pregunta = "¿Cuál es el código de autorización para reembolsos?"
        
        print(f"Consultando: {pregunta}")
        respuesta = query_engine.query(pregunta)

        print(f"\n✅ RESPUESTA: {respuesta}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ejecutar_rag()