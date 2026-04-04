import os
from dotenv import load_dotenv
# Componentes de LlamaIndex
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.langchain import LangchainEmbedding
# Componente puente de LangChain
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- CONFIGURACIÓN CORRECTA ---

# 1. El Cerebro (LLM) - Usamos el 2.5 que es tu éxito
Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash", 
    api_key=api_key
)

# 2. La Vista (Embeddings) - Usamos el nombre exacto que validaste
lc_embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", # EL NOMBRE CORRECTO
    google_api_key=api_key
)
Settings.embed_model = LangchainEmbedding(lc_embed_model)

def ejecutar_agente():
    print("🚀 Iniciando Agente Technova (Versión Corregida)...")
    try:
        # Carga el manual (ajustá la ruta si es necesario)
        documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()
        
        # Crea el índice
        index = VectorStoreIndex.from_documents(documents)
        
        # Motor de consulta
        query_engine = index.as_query_engine()
        
        # La pregunta del manual
        respuesta = query_engine.query("¿Cuál es el código de autorización para reembolsos?")
        
        print("\n" + "="*50)
        print(f"RESULTADO: {respuesta}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error técnico: {e}")

if __name__ == "__main__":
    ejecutar_agente()