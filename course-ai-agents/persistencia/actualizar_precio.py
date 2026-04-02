import sqlite3

def actualizar_monitor():
    # 1. Abrimos el archivo
    conexion = sqlite3.connect("technova.db")
    cursor = conexion.cursor()

    print("Cambiando el precio del Monitor (ID 2)...")

    # 2. Mandamos la orden a la 'sala de espera'
    # Cambiamos el precio a 450 para el producto con ID 2
    cursor.execute("UPDATE productos SET precio = 450 WHERE id = 2")

    # 3. EL PASO SAGRADO: Guardar los cambios en el disco duro
    # Sin esta línea, el archivo technova.db NO se modifica
    conexion.commit() 
    print("¡Cambio guardado con éxito!")

    # 4. Verificamos que realmente cambió
    cursor.execute("SELECT nombre, precio FROM productos WHERE id = 2")
    resultado = cursor.fetchone()
    print(f"Verificación: {resultado[0]} ahora cuesta ${resultado[1]}")

    # 5. Cerramos todo
    conexion.close()

if __name__ == "__main__":
    actualizar_monitor()
