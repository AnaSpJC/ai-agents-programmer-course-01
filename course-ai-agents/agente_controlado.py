import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Prompt ultra-preciso
instrucciones = "Eres un Mentor de soporte. Analiza el correo en ### y responde con un objeto JSON que tenga las llaves: 'urgencia', 'sentimiento' y 'consejo'."
correo_usuario = "¡El servicio es un desastre! Hace tres días que espero. Quiero soluciones ya."

# --- CONFIGURACIÓN PROFESIONAL ---
config_pro = types.GenerateContentConfig(
    temperature=0.9, # Alta, creativo
    max_output_tokens=1000, # Aumentamos el margen
    response_mime_type="application/json" # <--- Esto fuerza a la IA a dar solo el JSON puro
)

print("Solicitando respuesta...")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{instrucciones}\n\n###\n{correo_usuario}\n###",
        config=config_pro
    )
    print(response.text)
except Exception as e:
    print(f"Error: {e}")