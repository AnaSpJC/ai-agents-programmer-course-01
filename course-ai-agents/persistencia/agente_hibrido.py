import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. IMPORTACIÓN: Traemos las funciones puras de SQL
from agente_sql_tools import consultar_precio_sql, registrar_venta_sql

load_dotenv()

# --- CONFIGURACIÓN DE MODELOS ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# --- CONFIGURACIÓN DE CHROMADB ---
client = chromadb.PersistentClient(path="./chroma_db")
coleccion = client.get_or_create_collection(name="politicas_empresa")

# --- 2. ENVOLTORIOS (TOOLS): Aquí las hacemos "profesionales" para la IA ---

@tool
def tool_consultar_precio(nombre_producto: str) -> str:
    """Busca el precio de un producto en la base de datos de Tech-Nova usando SQL."""
    # Llamamos a la función que importamos arriba
    return consultar_precio_sql(nombre_producto)

@tool
def tool_registrar_venta(nombre_producto: str) -> str:
    """Registra la venta y descuenta 1 del stock. Úsala solo si el cliente confirma la compra."""
    return registrar_venta_sql(nombre_producto)

@tool
def tool_consultar_politicas(consulta: str) -> str:
    """Consulta las políticas de la empresa, métodos de pago y devoluciones usando búsqueda semántica."""
    vector_busqueda = embeddings_model.embed_query(consulta)
    resultado = coleccion.query(query_embeddings=[vector_busqueda], n_results=1)
    if resultado['documents']:
        return f"Política encontrada: {resultado['documents'][0][0]}"
    return "No hay información sobre esa política."

# --- 3. LISTA DE TOOLS UNIFICADA ---
# Usamos los nombres de las funciones que tienen el @tool arriba
tools = [tool_consultar_precio, tool_registrar_venta, tool_consultar_politicas]

# --- 4. ORQUESTADOR ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres el asistente experto de Tech-Nova. Tienes acceso a SQL para precios y a Vectores para políticas. Responde de forma concisa."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- BUCLE DE CHAT ---
chat_history = []
print("\n=== TECH-NOVA: SISTEMA HÍBRIDO (SQL + RAG) ===\n")

while True:
    user_query = input("Cliente: ")
    if user_query.lower() in ["salir", "exit"]: break

    resultado = agent_executor.invoke({"input": user_query, "chat_history": chat_history})
    
    # Manejo de la respuesta limpia
    output = resultado['output']
    texto_final = output[0].get('text') if isinstance(output, list) else output

    print(f"Agente: {texto_final}")
    
    chat_history.append(HumanMessage(content=user_query))
    chat_history.append(AIMessage(content=texto_final))