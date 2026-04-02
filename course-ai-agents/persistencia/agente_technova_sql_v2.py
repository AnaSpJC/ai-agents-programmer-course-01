import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# IMPORTANTE: Importamos tus funciones de persistencia
from agente_sql_tools import consultar_precio_sql, registrar_venta_sql

load_dotenv()

# 1. Definimos las Herramientas (Tools) usando el decorador que YA conoces
@tool
def tool_consultar_precio(nombre_producto: str):
    """Consulta el precio de un producto en la base de datos de Tech-Nova."""
    return consultar_precio_sql(nombre_producto)

@tool
def tool_registrar_venta(nombre_producto: str):
    """Registra la venta de un producto y descuenta 1 del stock en la base de datos."""
    return registrar_venta_sql(nombre_producto)

tools = [tool_consultar_precio, tool_registrar_venta]

# 2. Configuración del Modelo
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 3. El Prompt (Tu mapa de comportamiento)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres el asistente experto de Tech-Nova. Usas SQL para dar datos precisos."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Creación del Agente (Forma moderna y compatible)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Memoria manual (Para que no te confunda el BufferMemory)
chat_history = []

print("--- Tech-Nova SQL Agent (Versión Corregida) Activo ---")

while True:
    usuario = input("\nCliente: ")
    if usuario.lower() in ["salir", "exit"]:
        break
    
    # Ejecución
    resultado = agent_executor.invoke({
        "input": usuario,
        "chat_history": chat_history
    })
    
    respuesta_final = resultado["output"]
    
    # Guardamos en memoria
    chat_history.append(("human", usuario))
    chat_history.append(("ai", respuesta_final))
    
    print(f"\nAgente: {respuesta_final}")