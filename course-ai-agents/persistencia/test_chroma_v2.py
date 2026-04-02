import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# 1. El Traductor
# Probamos con el nombre técnico directo. Si este falla, el error es de permisos de API.
try:
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # Test rápido antes de seguir
    test_vector = embeddings_model.embed_query("test")
    print("Conexión con el modelo de embeddings: EXITOSA")
except Exception:
    print("Fallo text-embedding-004, intentando modelo de respaldo...")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 2. El Almacén (ChromaDB)
client = chromadb.PersistentClient(path="./chroma_db")
coleccion = client.get_or_create_collection(name="politicas_empresa")

# 3. "Sembrar" la información
textos = [
    "No hay devoluciones para drones usados más de 5 horas.",
    "Aceptamos criptomonedas como medio de pago únicamente los días jueves.",
    "El servicio técnico solo repara laptops y PCs, no electrodomésticos."
]
ids = ["id1", "id2", "id3"]

print("Procesando vectores...")

for i, texto in enumerate(textos):
    vector = embeddings_model.embed_query(texto)
    coleccion.upsert(
        embeddings=[vector],
        documents=[texto],
        ids=[ids[i]]
    )

# --- LA CONSULTA ---
pregunta_usuario = "¿Puedo pagar con Ethereum el martes?"
print(f"\nUsuario pregunta: {pregunta_usuario}")

vector_pregunta = embeddings_model.embed_query(pregunta_usuario)
resultado = coleccion.query(
    query_embeddings=[vector_pregunta],
    n_results=1 
)

print(f"\nRespuesta encontrada: {resultado['documents'][0][0]}")