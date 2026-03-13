import os
from google import genai
from dotenv import load_dotenv

# 1. Cargamos la llave de acceso
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Creamos el Cliente
# Eliminamos el 'http_options' que forzaba la v1 porque tu lista mostró que
# los modelos nuevos (2.5 y 3) prefieren la configuración por defecto.
client = genai.Client(api_key=api_key)

# 3. Tu PROMPT (El cerebro del agente)
instrucciones = """
Sos un experto en atención al cliente especializado en dudas y reclamos. 
Vas a recibir un correo de reclamo.
Analiza el correo encerrado en ###.
Debes:
1.- Extraer el problema principal.
2.- Clasificar urgencia: Alta, Media o Baja.
3.- Responder UNICAMENTE con este formato: [Nivel] - [Resumen de 5 palabras]
"""

# 4. El correo del usuario (El dato de entrada)
correo_usuario = "¡Es el colmo! Hace tres días que mi internet no funciona y trabajo desde casa. Nadie me da una solución."

# 5. Llamada al modelo 
# Usamos 'gemini-2.5-flash', que es el que apareció primero en tu lista oficial.
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"{instrucciones}\n\n###\n{correo_usuario}\n###"
)

# 6. Resultados
print("-" * 30)
print("RESPUESTA DEL AGENTE:")
print(response.text)
print("-" * 30)