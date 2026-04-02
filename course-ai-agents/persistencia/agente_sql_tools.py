import sqlite3

def conectar():
    """Función auxiliar para no repetir código de conexión."""
    return sqlite3.connect("technova.db")

def consultar_precio_sql(nombre_producto: str):
    """
    Busca el precio de un producto en la base de datos usando coincidencias parciales.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Usamos LIKE con % para que sea flexible (ej: 'mouse' encuentra 'Mouse Ergonómico')
    query = "SELECT nombre, precio FROM productos WHERE nombre LIKE ?"
    
    try:
        cursor.execute(query, (f"%{nombre_producto}%",))
        resultado = cursor.fetchone()
        
        if resultado:
            # resultado[0] es el nombre real, resultado[1] es el precio
            return f"El {resultado[0]} tiene un precio de {resultado[1]} USD."
        else:
            return f"Lo siento, no encontré el producto '{nombre_producto}' en el inventario."
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"
    finally:
        conexion.close()

def registrar_venta_sql(nombre_producto: str):
    """
    Resta 1 unidad de stock en la base de datos. 
    Solo si el producto existe y tiene stock > 0.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Query que intenta restar 1 si hay stock disponible
    query_update = "UPDATE productos SET stock = stock - 1 WHERE nombre LIKE ? AND stock > 0"
    
    try:
        cursor.execute(query_update, (f"%{nombre_producto}%",))
        
        # rowcount nos dice cuántas filas cambiaron de verdad
        if cursor.rowcount > 0:
            conexion.commit() # ¡BOTÓN DE GUARDAR!
            # Buscamos el stock restante para informar al usuario
            cursor.execute("SELECT stock FROM productos WHERE nombre LIKE ?", (f"%{nombre_producto}%",))
            nuevo_stock = cursor.fetchone()[0]
            return f"Venta registrada. El stock actualizado es de {nuevo_stock} unidades."
        else:
            return f"No se pudo realizar la venta. Verifica si '{nombre_producto}' tiene stock disponible."
    except Exception as e:
        return f"Error técnico al registrar la venta: {e}"
    finally:
        conexion.close()

# --- BLOQUE DE PRUEBA (Para que verifiques que todo anda bien) ---
if __name__ == "__main__":
    print("--- Probando Consultar ---")
    print(consultar_precio_sql("Monitor"))
    
    print("\n--- Probando Vender ---")
    print(registrar_venta_sql("Mouse"))