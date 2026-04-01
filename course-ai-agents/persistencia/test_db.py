import sqlite3

def probar_consultas():
    conexion = sqlite3.connect("technova.db")
    cursor = conexion.cursor()
    
    # --- CONSULTA 1: Todos los productos ---
    print("--- 1. TODOS LOS PRODUCTOS ---")
    cursor.execute("SELECT * FROM productos")
    todos = cursor.fetchall()
    for p in todos:
        print(f"[{p[0]}] {p[1]} - ${p[3]}")

    print("\n" + "-"*30 + "\n")

    # --- CONSULTA 2: Solo el ID 1 ---
    print("--- 2. SOLO EL PRODUCTO CON ID 1 ---")
    # Usamos la cláusula WHERE para filtrar
    cursor.execute("SELECT * FROM productos WHERE id = 1")
    producto_uno = cursor.fetchone() # Usamos fetchone porque sabemos que es solo uno
    
    if producto_uno:
        print(f"Encontrado: {producto_uno[1]} (Modelo: {producto_uno[2]})")
    else:
        print("No se encontró el producto con ID 1.")

    conexion.close()

if __name__ == "__main__":
    probar_consultas()