import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# 1. Configuración del Modelo (Gemini 2.5 Flash)
# No usamos Embeddings aquí para evitar el error 404
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# 2. Lectura directa del archivo (Python puro)
try:
    with open("mi_empresa.txt", "r", encoding="utf-8") as f:
        contexto_del_archivo = f.read()
    print("Archivo leído con éxito.")
except FileNotFoundError:
    contexto_del_archivo = "Error: El archivo mi_empresa.txt no existe."

# 3. La Pregunta
pregunta = "¿Cuál es el código de autorización para reembolsos y cuántos días tengo?"

# 4. El Prompt RAG Directo
# Metemos el contenido del archivo directo en las instrucciones
prompt = f"""Eres un asistente de atención al cliente. 
Usa la siguiente información para responder la pregunta. 
Si no está aquí, di que no lo sabes.

INFORMACIÓN DE LA EMPRESA:
{contexto_del_archivo}

PREGUNTA DEL USUARIO:
{pregunta}
"""

# 5. Respuesta
print("Consultando a Gemini 2.5...")
respuesta = llm.invoke(prompt)

print("-" * 30)
print(f"IA: {respuesta.content}")
print("-" * 30)