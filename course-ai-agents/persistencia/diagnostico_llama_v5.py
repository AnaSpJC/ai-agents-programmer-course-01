import os
from dotenv import load_dotenv
# Importamos las piezas que SÍ tienes instaladas
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

load_dotenv()

# Usamos la KEY que definiste en tu historial de errores
api_key = os.getenv("GEMINI_API_KEY")

# 1. CONFIGURACIÓN TÉCNICA
# Forzamos api_version="v1" para que NO intente entrar por v1beta (Error 404)
Settings.llm = Gemini(
    model="models/gemini-1.5-flash", 
    api_key=api_key,
    api_version="v1" 
)

# Usamos la clase de embeddings que tienes instalada
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/embedding-001",
    api_key=api_key
)

# 2. CARGA DE DATOS
# Asumimos que mi_empresa.txt está en la carpeta raíz (un nivel arriba de persistencia)
print("--- Leyendo manual de la empresa ---")
try:
    documents = SimpleDirectoryReader(input_files=["../mi_empresa.txt"]).load_data()
    
    # 3. CREACIÓN DEL ÍNDICE
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # 4. PRUEBA REAL
    pregunta = "¿Cuál es el código de autorización para reembolsos?"
    print(f"Preguntando: {pregunta}")
    respuesta = query_engine.query(pregunta)

    print("\n" + "="*40)
    print(f"RESULTADO: {respuesta}")
    print("="*40)

except Exception as e:
    print(f"❌ Error detectado: {e}")