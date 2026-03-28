import os
import re # Para el manejo de stock con números
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()

# --- FASE 1: CONOCIMIENTO ---
def cargar_inventario():
    with open("inventario.txt", "r", encoding="utf-8") as f:
        return f.read()

# --- FASE 2: HERRAMIENTAS (Incluyendo la nueva de Stock) ---

@tool
def aplicar_descuento_vip(precio: float) -> float:
    """Aplica un 15% de descuento. Úsala si el cliente confirma ser VIP."""
    return precio * 0.85

@tool
def calcular_costo_envio(destino: str) -> float:
    """Argentina: 10 USD. Otros: 50 USD. Necesita el país de destino."""
    return 10.0 if destino.lower() == "argentina" else 50.0

@tool
def registrar_compra_y_stock(nombre_producto: str) -> str:
    """
    Resta 1 unidad del stock en inventario.txt. 
    Úsala SOLO cuando el cliente diga 'comprar', 'lo quiero', o confirme la transacción.
    """
    archivo = "inventario.txt"
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        
        producto_encontrado = False
        for i, linea in enumerate(lineas):
            if f"PRODUCTO: {nombre_producto}" in linea:
                producto_encontrado = True
                # Buscamos la línea de STOCK que sigue (máximo 3 líneas abajo)
                for j in range(1, 4):
                    if i + j < len(lineas) and "STOCK:" in lineas[i+j]:
                        stock_actual = int(re.search(r'\d+', lineas[i+j]).group())
                        if stock_actual > 0:
                            nuevo_stock = stock_actual - 1
                            lineas[i+j] = f"STOCK: {nuevo_stock} unidades\n"
                            with open(archivo, "w", encoding="utf-8") as f_out:
                                f_out.writelines(lineas)
                            return f"Éxito: Venta registrada. Nuevo stock de {nombre_producto}: {nuevo_stock}."
                        else:
                            return f"Error: No queda stock de {nombre_producto}."
        return f"Error: No encontré el producto '{nombre_producto}'."
    except Exception as e:
        return f"Error técnico al actualizar stock: {e}"

tools = [aplicar_descuento_vip, calcular_costo_envio, registrar_compra_y_stock]

# --- FASE 3: EL ORQUESTADOR ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Eres el asistente de Tech-Nova. Inventario actual:\n{cargar_inventario()}
    INSTRUCCIONES:
    1. Usa las tools para precios, envíos y descuentos.
    2. Si el usuario decide comprar, DEBES llamar a 'registrar_compra_y_stock'.
    3. Responde siempre de forma amable."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"), 
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- BUCLE DE CHAT ---
chat_history = []
print("\n=== TECH-NOVA: SISTEMA INTEGRAL (Venta + Stock + Memoria) ===\n")

while True:
    user_query = input("Tú: ")
    if user_query.lower() in ["salir", "exit", "chau"]: break

    resultado = agent_executor.invoke({"input": user_query, "chat_history": chat_history})
    
    # Limpieza de salida
    respuesta_final = resultado['output']
    texto_limpio = respuesta_final[0].get('text') if isinstance(respuesta_final, list) else respuesta_final

    print(f"ASISTENTE: {texto_limpio}")

    chat_history.append(HumanMessage(content=user_query))
    chat_history.append(AIMessage(content=texto_limpio))