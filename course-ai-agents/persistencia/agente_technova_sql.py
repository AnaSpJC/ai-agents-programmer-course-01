import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory

# IMPORTANTE: Importamos tus funciones de persistencia
from agente_sql_tools import consultar_precio_sql, registrar_venta_sql

# 1. Configuración del Modelo
# Asegúrate de tener tu API KEY en las variables de entorno
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# 2. Definición de las "Manos" del Agente (Tools)
tools = [
    Tool(
        name="ConsultarPrecio",
        func=consultar_precio_sql,
        description="Útil para cuando el usuario pregunta el precio de un producto. Entrada: nombre del producto."
    ),
    Tool(
        name="RegistrarVenta",
        func=registrar_venta_sql,
        description="Útil para cuando el usuario confirma que quiere comprar un producto. Resta 1 del stock. Entrada: nombre del producto."
    )
]

# 3. Memoria de la conversación
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 4. Inicialización del Agente Profesional
agente = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True, # Para que veas cómo "piensa" y qué SQL llama
    memory=memory
)

# 5. El System Prompt (Las reglas de comportamiento)
SISTEMA = """Eres el asistente de ventas de Tech-Nova. 
Tu objetivo es ayudar a los clientes con precios y compras.
IMPORTANTE: 
1. Si el cliente quiere comprar, DEBES usar la herramienta RegistrarVenta.
2. Siempre responde de forma profesional y directa.
3. Si no encuentras un producto, ofrece disculpas."""

# --- Bucle de Chat ---
print("--- Tech-Nova SQL Agent Activo ---")
while True:
    usuario = input("\nCliente: ")
    if usuario.lower() in ["salir", "exit", "chau"]:
        break
    
    # El agente procesa la entrada usando las herramientas SQL
    respuesta = agente.run(input=f"{SISTEMA}\n\nUsuario: {usuario}")
    print(f"\nAgente: {respuesta}")