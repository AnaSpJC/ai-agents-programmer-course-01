import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# 1. Configuramos el modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

# 2. Plantilla con ESPACIO PARA MEMORIA
# "history" es el nombre que le damos a nuestra lista de recuerdos
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente amable. Recuerda siempre el nombre del usuario."),
    MessagesPlaceholder(variable_name="history"), 
    ("user", "{input}")
])

# 3. La Cadena (Chain)
chain = prompt | llm

# 4. SIMULACIÓN DE MEMORIA (Historial Manual)
# En el Módulo 3 avanzado esto se guarda en bases de datos, 
# pero hoy lo haremos con una lista de Python para que entiendas la lógica.
historial = []

# --- PRIMER TURNO ---
print("Turno 1: Presentación")
user_input_1 = "Hola, me llamo Ana."
respuesta_1 = chain.invoke({"input": user_input_1, "history": historial})

# Guardamos lo que pasó en el historial
historial.append(HumanMessage(content=user_input_1))
historial.append(AIMessage(content=respuesta_1.content))

print(f"IA: {respuesta_1.content}")

# --- SEGUNDO TURNO (Aquí ocurre la magia) ---
print("\nTurno 2: La prueba de memoria")
user_input_2 = "¿Te acordás cómo me llamo?"
# Le pasamos el historial que ya tiene guardado el nombre
respuesta_2 = chain.invoke({"input": user_input_2, "history": []})

print(f"IA: {respuesta_2.content}")