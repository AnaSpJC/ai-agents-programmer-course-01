import requests # Aquí importamos lo que instalamos con pip

def probar_conexion():
    url = "https://api.github.com"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        print("✅ ¡Éxito! Tu entorno está listo para conectar con APIs de IA.")
    else:
        print("❌ Algo salió mal con la conexión.")

probar_conexion()