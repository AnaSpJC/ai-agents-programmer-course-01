'''1.	Define una función llamada calcular_costo que reciba un parámetro llamado tokens.
2.	Dentro de la función, multiplica tokens por 0.00002 (el costo imaginario por cada token).
3.	Usa return para devolver ese resultado.
4.	Fuera de la función, crea una variable mis_tokens = 5000.
5.	Llama a tu función pasando esa variable y guarda el resultado en una variable llamada total.
6.	Imprime un mensaje que diga: "El costo total de la consulta es: [total] USD".
'''
def calcular_costo (tokens):
    costo = tokens * 0.00002
    return costo

mis_tokens = 5000

total = calcular_costo(mis_tokens)
print(f"El costo total de la consulta es: {total} USD")