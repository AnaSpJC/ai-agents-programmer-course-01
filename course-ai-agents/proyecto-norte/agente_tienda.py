import os
from dotenv import load_dotenv

# Importaciones necesarias para el Agente Autónomo
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- FASE 1: CONOCIMIENTO (Inventario) ---
def cargar_inventario():
    with open("inventario.txt", "r", encoding="utf-8") as f:
        return f.read()

contexto_tienda = cargar_inventario()

# --- FASE 2: HERRAMIENTAS (Habilidades) ---
@tool
def aplicar_descuento_vip(precio: float) -> float:
    """Aplica un 15% de descuento. Úsala si el cliente dice ser VIP o Premium."""
    return precio * 0.85

@tool
def calcular_costo_envio(destino: str) -> float:
    """Calcula envío. Argentina: 10 USD. Otros países: 50 USD. Necesita el país."""
    if destino.lower() == "argentina":
        return 10.0
    return 50.0

tools = [aplicar_descuento_vip, calcular_costo_envio]

# --- FASE 3: EL MOTOR (AgentExecutor) ---

# 1. El Cerebro
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 2. El Plano de Razonamiento (Prompt)
# {agent_scratchpad} es indispensable: es donde la IA anota sus "pensamientos"
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente oficial de Tech-Nova. 
    Usa este inventario para responder sobre productos:
    {contexto_tienda}
    
    Si necesitas calcular descuentos o envíos, USA LAS HERRAMIENTAS.
    No inventes precios finales sin usar la herramienta correspondiente."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), 
])

# 3. Construir el Agente (Une LLM + Tools + Prompt)
agent = create_tool_calling_agent(llm, tools, prompt)

# 4. Crear el Ejecutor (El que hace el trabajo sucio)
# verbose=True es VITAL para que veas el razonamiento en la terminal
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- PRUEBA FINAL DEL PROYECTO NORTE ---
pregunta_usuario = "Soy VIP de Uruguay y quiero comprar el Mouse Ergonómico. ¿Cuál es el precio final con envío?"

print(f"Pregunta: {pregunta_usuario}")
resultado = agent_executor.invoke({"input": pregunta_usuario})

print("-" * 30)
print(f"RESPUESTA AL CLIENTE: {resultado['output']}")
print("-" * 30)