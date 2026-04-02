import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# 1. El Traductor (Modelo de Embeddings ACTUALIZADO a 2026)
# Cambiamos 'embedding-001' por 'text-embedding-004'
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

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

print("Convirtiendo textos a vectores y guardando en ChromaDB...")

# Eliminamos duplicados si corres el script varias veces
for i, texto in enumerate(textos):
    vector = embeddings_model.embed_query(texto)
    coleccion.upsert( # Usamos upsert para que no de error si el ID ya existe
        embeddings=[vector],
        documents=[texto],
        ids=[ids[i]]
    )

print("¡Base de datos de vectores lista!")

# --- LA PREGUNTA TRAMPA ---
pregunta_usuario = "¿Puedo pagar con Ethereum el martes?"
print(f"\nUsuario pregunta: {pregunta_usuario}")

vector_pregunta = embeddings_model.embed_query(pregunta_usuario)

resultado = coleccion.query(
    query_embeddings=[vector_pregunta],
    n_results=1 
)

print(f"\nRespuesta encontrada por significado: {resultado['documents'][0][0]}")