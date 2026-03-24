import os
from dotenv import load_dotenv

# 1. El Cerebro
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# 2. EL MOTOR (langchain_classic)
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()

# --- FASE 1: CONOCIMIENTO ---
def cargar_inventario():
    with open("inventario.txt", "r", encoding="utf-8") as f:
        return f.read()

contexto_tienda = cargar_inventario()

# --- FASE 2: HERRAMIENTAS ---
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

# --- FASE 3: EL ORQUESTADOR ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente oficial de Tech-Nova. 
    Usa este inventario para responder sobre productos:
    {contexto_tienda}
    
    Si necesitas calcular descuentos o envíos, USA LAS HERRAMIENTAS.
    No inventes precios finales sin usar la herramienta correspondiente."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), 
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- NUEVA FASE DE EJECUCIÓN: BUCLE DE CHAT ---
print("\n" + "="*40)
print("SISTEMA TECH-NOVA ONLINE")
print("Escribe 'salir' para finalizar la charla.")
print("="*40 + "\n")

while True:
    # 1. Capturamos lo que escribes en la terminal
    user_query = input("Tú: ")

    # 2. Verificamos si quieres cerrar el chat
    if user_query.lower() in ["salir", "exit", "quit", "chau"]:
        print("Asistente: ¡Gracias por contactar a Tech-Nova! Hasta pronto.")
        break

    # 3. El agente procesa tu entrada y genera la respuesta
    # Nota: El input ahora viene de la terminal, no de una variable fija
    try:
        resultado = agent_executor.invoke({"input": user_query})
        
        # Extraemos la respuesta final
        respuesta_final = resultado['output']
    
        # Si la respuesta es una lista (como te pasó recién), tomamos el texto del primer elemento
        if isinstance(respuesta_final, list) and len(respuesta_final) > 0:
            texto_limpio = respuesta_final[0].get('text', str(respuesta_final[0]))
        else:
            texto_limpio = respuesta_final
        print("-" * 30)
        print(f"ASISTENTE: {texto_limpio}")
        print("-" * 30)
    except Exception as e:
        print(f"Ocurrió un error: {e}")