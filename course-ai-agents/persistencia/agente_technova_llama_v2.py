import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. LLM (Tu éxito validado)
Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash", 
    api_key=api_key
)

# 2. EMBEDDINGS (El cambio crítico)
# Usamos 'models/embedding-001'. Es el modelo base que 
# Google garantiza compatibilidad incluso en rutas v1beta.
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/embedding-001", 
    api_key=api_key
)

def iniciar_agente_lector():
    print("--- BLOQUE 3: REINTENTO DE INDEXACIÓN ---")
    try:
        print("📖 Cargando manual...")
        documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()

        print("🧠 Generando vectores con embedding-001...")
        # Aquí es donde fallaba antes
        index = VectorStoreIndex.from_documents(documents)

        print("🔍 Creando motor de consulta...")
        query_engine = index.as_query_engine()

        pregunta = "¿Cuál es el código de autorización para reembolsos?"
        respuesta = query_engine.query(pregunta)
        
        print("\n" + "="*50)
        print(f"IA: {respuesta}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")

if __name__ == "__main__":
    iniciar_agente_lector()