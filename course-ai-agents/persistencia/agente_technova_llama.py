import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. CONFIGURACIÓN BASADA EN TU ÉXITO (v8 modificado)
# Usamos el 2.5 que es el que te respondió "¡Hola!"
Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash", 
    api_key=api_key
)

# 2. CONFIGURACIÓN DE EMBEDDINGS
# Para que LlamaIndex pueda "leer" el manual, necesita este motor de vectores
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/text-embedding-004", 
    api_key=api_key
)

def iniciar_agente_lector():
    print("--- BLOQUE 3: LECTURA DE MANUAL CON GEMINI 2.5 ---")
    try:
        # Carga el manual desde la raíz del proyecto
        print("📖 Cargando manual de la empresa...")
        documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()

        # Crea el índice (aquí es donde se usa el embedding)
        print("🧠 Indexando conocimientos...")
        index = VectorStoreIndex.from_documents(documents)

        # Crea el motor de consultas
        query_engine = index.as_query_engine()

        # Prueba de consulta real
        pregunta = "¿Cuál es el código de autorización para reembolsos?"
        print(f"❓ Pregunta: {pregunta}")
        
        respuesta = query_engine.query(pregunta)
        
        print("\n" + "="*50)
        print(f"RESPUESTA DEL AGENTE: {respuesta}")
        print("="*50)

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")

if __name__ == "__main__":
    iniciar_agente_lector()