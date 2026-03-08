'''1.	Crea una lista llamada herramientas que contenga tres strings: "google_search", "calculadora",
         y "traductor".
2.	Crea un diccionario llamado agente que tenga tres claves:
    o	nombre: (ponle el nombre que quieras a tu agente).
    o	version: (un número decimal, por ejemplo 1.0).
    o	esta_activo: (un valor booleano: True o False).
3.	Usa el comando print() para mostrar en la consola el nombre de tu agente y la segunda herramienta 
    de tu lista.
'''
herramientas = ["google_search", "calculadora", "traductor"]
agente = {
    "nombre": "Gemma",
    "version": 1.0,
    "esta_activo": True
}
print(agente["nombre"], herramientas[1])
print(f"El nombre de mi agente es {agente["nombre"]} y la herramienta solicitada es {herramientas[1]}")