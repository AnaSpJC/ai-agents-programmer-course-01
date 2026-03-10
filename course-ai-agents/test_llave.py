import os
from dotenv import load_dotenv

# Esto carga los datos del archivo .env a la memoria
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"✅ ¡Conseguido! La llave termina en: ...{api_key[-4:]}")
    print("Estamos listos para el Módulo 2.")
else:
    print("❌ No encuentro la llave. Revisa el archivo .env")