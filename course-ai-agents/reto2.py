'''El Escenario: Imagina que tu agente recibe una lista de mensajes del usuario. 
Tu trabajo es filtrar cuáles son "comandos" y cuáles son solo "saludos".
Tu tarea:
1.	Crea una lista llamada mensajes con estos textos: "hola", "buscar", "clima", "gracias", "ayuda".
2.	Crea un bucle for que recorra esa lista.
3.	Dentro del bucle, usa un if para verificar:
    o	Si el mensaje es "buscar" o "clima", imprime: "Ejecutando acción para: [mensaje]".
    o	Si el mensaje es "ayuda", imprime: "Mostrando menú de asistencia".
    o	Para cualquier otro mensaje (como "hola" o "gracias"), imprime: "Ignorando charla trivial".
'''
mensajes = ["hola", "buscar", "clima", "gracias", "ayuda"]

for m in mensajes:
    if m == "buscar" or m == "clima":
        print(f"Ejecutando acción para: {m}")
    elif m == "ayuda":
        print("Mostrando menú de asistencia")
    else:
        print("Ignorando charla trivial")