'''Crea un archivo llamado diagnostico.py y escribe un pequeño script que tenga una lista de diccionarios
 (por ejemplo, tres usuarios con nombre y edad) y que use un ciclo for para imprimir
 solo los nombres de los que son mayores de 18.'''

usu = [
    {
        "nombre": "a",
        "edad": 16
    },
    {
        "nombre": "b",
        "edad": 19
    },
    {
        "nombre": "a",
        "edad": 18
    }
 ]
for usuario in  usu:
    if usuario["edad"] > 18:
        print (usuario["nombre"])