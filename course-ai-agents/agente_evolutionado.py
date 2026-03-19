import os
from google import genai
from dotenv import load_dotenv

# 1. Configuración de entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. PROMPT EVOLUCIONADO (Tema 3: Rol + Contexto + Tarea + Formato)
# Aquí aplicamos "Few-shot" implícito al definir la estructura JSON esperada.
instrucciones = """
Eres un Mentor Senior de Atención al Cliente, experto en psicología del consumidor.
Tu tarea es analizar correos de clientes y preparar al empleado que los atenderá.

Debes analizar el correo encerrado en ### y responder ÚNICAMENTE en formato JSON:

{
  "urgencia": "Alta | Media | Baja",
  "sentimiento_cliente": "Describí el humor del cliente en 1 palabra",
  "problema_detectado": "Resumen de 5 palabras del problema técnico o comercial",
  "estrategia_mentor": "Un consejo de cómo hablarle para calmarlo o cerrar la venta"
}
"""

# 3. CASO DE PRUEBA (El cliente "Multitarea" y enojado)
correo_usuario = """
¡Es increíble! El servicio es malísimo. Además de que ayer se cortó, 
estoy viendo la factura y me parece un robo. 
¿Cuánto sale el plan premium? Porque si voy a pagar esta fortuna, 
al menos quiero la velocidad que prometen. ¡Contesten rápido!
"""

# 4. Ejecución
print("Generando análisis estratégico...")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{instrucciones}\n\n###\n{correo_usuario}\n###"
    )

    print("-" * 30)
    print("ANÁLISIS DEL MENTOR (JSON):")
    print(response.text)
    print("-" * 30)

except Exception as e:
    print(f"Error inesperado: {e}")
