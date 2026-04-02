import os
from dotenv import load_dotenv

# USAMOS TUS IMPORTACIONES PROBADAS (langchain_classic)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

# Importamos tus funciones de la base de datos
from agente_sql_tools import consultar_precio_sql, registrar_venta_sql

load_dotenv()

# --- FASE 1: HERRAMIENTAS SQL ---

@tool
def tool_consultar_precio(nombre_producto: str) -> str:
    """Busca el precio de un producto en la base de datos profesional de Tech-Nova."""
    return consultar_precio_sql(nombre_producto)

@tool
def tool_registrar_venta(nombre_producto: str) -> str:
    """Registra la venta y descuenta 1 del stock en la base de datos SQL. Úsala solo si el cliente confirma la compra."""
    return registrar_venta_sql(nombre_producto)

tools = [tool_consultar_precio, tool_registrar_venta]

# --- FASE 2: EL ORQUESTADOR ---
# Usamos el modelo que ya probaste (gemini-2.5-flash)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres el asistente experto de Tech-Nova. Tu base de datos es SQL y debes usar tus tools para dar información precisa."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), # Mantenemos tu sintaxis de placeholder
])

# Construcción con tus librerías 'classic'
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- BUCLE DE CHAT ---
chat_history = []
print("\n=== TECH-NOVA: SISTEMA SQL PROFESIONAL (Fase 1 completada) ===\n")

while True:
    user_query = input("Tú: ")
    if user_query.lower() in ["salir", "exit", "chau"]: break

    # Ejecución con tu formato de invoke
    resultado = agent_executor.invoke({"input": user_query, "chat_history": chat_history})
    
    # Manejo de respuesta (tu lógica de limpieza)
    respuesta_final = resultado['output']
    texto_limpio = respuesta_final[0].get('text') if isinstance(respuesta_final, list) else respuesta_final

    print(f"ASISTENTE: {texto_limpio}")

    # Memoria con tus clases HumanMessage y AIMessage
    chat_history.append(HumanMessage(content=user_query))
    chat_history.append(AIMessage(content=texto_limpio))