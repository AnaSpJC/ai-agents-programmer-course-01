import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# 1. Configuración del Motor (Gemini 2.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # El modelo que validamos
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0 # Queremos precisión, no creatividad
)

# 2. Carga de Conocimiento (Solución adoptada: Lectura Directa)
def cargar_contexto(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

contexto_empresa = cargar_contexto("mi_empresa.txt")

# 3. Construcción del Flujo de Agente
pregunta_usuario = "¿Cuál es el código de reembolso y cuántos días tengo?"

mensajes = [
    SystemMessage(content=f"""Eres un agente experto en soporte corporativo. 
    Tu única fuente de verdad es el siguiente manual:
    ----------
    {contexto_empresa}
    ----------
    Si la respuesta no está en el manual, responde: 'Lo siento, no tengo acceso a esa información específica'."""),
    HumanMessage(content=pregunta_usuario)
]

# 4. Ejecución
print("Consultando al Agente...")
respuesta = llm.invoke(mensajes)

print("\n" + "="*40)
print(f"RESPUESTA: {respuesta.content}")
print("="*40)
