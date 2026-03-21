import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser # <--- La nueva pieza

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

# Tu template perfecto
template = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor profesional. Traduce el texto al idioma {idioma} y determina el tono ({tono}). Responde así Traducción: [Aquí el texto] | Tono: [Aquí el tono]."),
    ("user", "Traducí esto: {texto}")
])

# 3. Definimos el Parser
parser = StrOutputParser()

# 4. LA CADENA EVOLUCIONADA
# Le sumamos el parser al final del flujo
chain = template | llm | parser 

# 5. Ejecución
print("Traduciendo con cadena profesional...")
respuesta = chain.invoke({
    "idioma": "Inglés",
    "tono": "Informal",
    "texto": "Hola mundo, qué día tan lindo"
})

print("-" * 30)
print(respuesta) # ¡Ahora 'respuesta' ya es un texto, no un objeto!
print("-" * 30)