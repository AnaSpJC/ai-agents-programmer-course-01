import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Cargar entorno
load_dotenv()

# 2. Configurar el Modelo (Nivel Profesional)
# Aquí usamos la clase específica de LangChain para Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Crear la Plantilla (Prompt Template)
# Las llaves {tema} y {cliente} son espacios que llenaremos después
template = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en soporte técnico. Tu objetivo es resumir el problema en 3 palabras."),
    ("user", "Hola, tengo un problema con mi {tema}. El cliente dice: {cliente}")
])

# 4. Unir todo en una Cadena (Chain)
# El símbolo '|' se llama "pipe" y sirve para conectar las piezas
chain = template | llm

# 5. Ejecutar la cadena
print("Ejecutando cadena de LangChain...")
respuesta = chain.invoke({
    "tema": "Internet",
    "cliente": "No me carga ninguna página desde ayer a la tarde."
})

print("-" * 30)
print("RESPUESTA:")
print(respuesta.content) # En LangChain usamos .content
print("-" * 30)