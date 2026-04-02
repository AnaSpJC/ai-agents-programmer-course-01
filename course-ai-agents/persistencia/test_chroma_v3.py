import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# 1. El Traductor (USANDO TU MODELO COMPROBADO)
# Usamos el nombre exacto que salió en tu lista
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. El Almacén (ChromaDB)
# Esto creará la carpeta 'chroma_db' en tu directorio actual
client = chromadb.PersistentClient(path="./chroma_db")
coleccion = client.get_or_create_collection(name="politicas_empresa")

# 3. "Sembrar" la información
textos = [
    "No hay devoluciones para drones usados más de 5 horas.",
    "Aceptamos criptomonedas como medio de pago únicamente los días jueves.",
    "El servicio técnico solo repara laptops y PCs, no electrodomésticos."
]
ids = ["id1", "id2", "id3"]

print("Generando vectores con gemini-embedding-001...")

for i, texto in enumerate(textos):
    # Generamos el vector
    vector = embeddings_model.embed_query(texto)
    # Lo guardamos o actualizamos
    coleccion.upsert(
        embeddings=[vector],
        documents=[texto],
        ids=[ids[i]]
    )

print("¡Base de datos de vectores lista y sembrada!")

# --- LA PRUEBA DE FUEGO ---
pregunta_usuario = "¿Puedo pagar con Ethereum el martes?"
print(f"\nUsuario pregunta: {pregunta_usuario}")

# Convertimos la pregunta usando EL MISMO modelo
vector_pregunta = embeddings_model.embed_query(pregunta_usuario)

# Buscamos similitud
resultado = coleccion.query(
    query_embeddings=[vector_pregunta],
    n_results=1 
)

print(f"\nRespuesta encontrada por significado: {resultado['documents'][0][0]}")