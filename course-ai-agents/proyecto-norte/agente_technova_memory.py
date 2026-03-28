import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
# IMPORTANTE: Necesitamos estos tipos de mensajes para la memoria
from langchain_core.messages import HumanMessage, AIMessage 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()

# --- FASE 1: CONOCIMIENTO (Igual) ---
def cargar_inventario():
    with open("inventario.txt", "r", encoding="utf-8") as f:
        return f.read()
contexto_tienda = cargar_inventario()

# --- FASE 2: HERRAMIENTAS (Igual) ---
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

# --- FASE 3: EL ORQUESTADOR CON MEMORIA ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# CAMBIO 1: Agregamos el 'MessagesPlaceholder' al prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", f"Eres el asistente oficial de Tech-Nova. Inventario:\n{contexto_tienda}"),
    MessagesPlaceholder(variable_name="chat_history"), # Aquí se inyectará la memoria
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), 
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- BUCLE DE CHAT INTERACTIVO ---
# CAMBIO 2: Inicializamos la lista de historial
chat_history = [] 

print("\nSISTEMA CON MEMORIA ACTIVO. Escribe 'salir' para finalizar.\n")

while True:
    user_query = input("Tú: ")
    if user_query.lower() in ["salir", "exit", "chau"]:
        break

    try:
        # CAMBIO 3: Pasamos el historial en cada invocación
        resultado = agent_executor.invoke({
            "input": user_query,
            "chat_history": chat_history # Le pasamos lo que recordamos
        })
        
        # Limpieza de la salida (lo que hablamos antes)
        respuesta_final = resultado['output']
        if isinstance(respuesta_final, list) and len(respuesta_final) > 0:
            texto_limpio = respuesta_final[0].get('text', str(respuesta_final[0]))
        else:
            texto_limpio = respuesta_final

        print(f"ASISTENTE: {texto_limpio}")

        # ACTUALIZACIÓN DE MEMORIA: Guardamos el intercambio actual
        chat_history.append(HumanMessage(content=user_query))
        chat_history.append(AIMessage(content=texto_limpio))

    except Exception as e:
        print(f"Error: {e}")