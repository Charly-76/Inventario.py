import sqlite3
conexion = sqlite3.connect ("inventario.db")
cursor = conexion.cursor()

from colorama import init, Fore, Style

print (Fore.WHITE + " =================================================================")
print (Fore.RED + " ********** Bienvenido a la Base de datos Inventario.db ********** ")
print (Fore.WHITE + " =================================================================")

# Inicializar colorama para colores en consola
init(autoreset=True)

# -------------------- BASE DE DATOS --------------------

def conectar():
    """Establece conexión con la base de datos SQLite 'inventario.db'."""
    return sqlite3.connect('inventario.db')

def crear_tabla():
    """
    Crea la tabla 'productos' si no existe,
    con las columnas id, nombre, descripcion, cantidad, precio, categoria.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

# -------------------- FUNCIONES CRUD --------------------

def registrar_producto():
    """Solicita datos y registra un nuevo producto."""
    print(Fore.CYAN + "\n--- Registrar nuevo producto ---")
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    categoria = input("Categoría: ")
    while True:
        try:
            cantidad = int(input("Cantidad disponible: "))
            break
        except ValueError:
            print(Fore.RED + "Cantidad debe ser número entero.")
    while True:
        try:
            precio = float(input("Precio: "))
            break
        except ValueError:
            print(Fore.RED + "Precio debe ser un número válido.")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto registrado con éxito.")

def ver_productos():
    """Muestra todos los productos registrados."""
    print(Fore.CYAN + "\n--- Lista de productos ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()

    if productos:
        for p in productos:
            print(f"{Fore.YELLOW}ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, "
                  f"Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
    else:
        print(Fore.RED + "No hay productos registrados.")

def buscar_producto_por_id():
    """Busca producto por ID y lo muestra si existe."""
    print(Fore.CYAN + "\n--- Buscar producto por ID ---")
    id_prod = input("ID: ")
    if not id_prod.isdigit():
        print(Fore.RED + "ID inválido, debe ser número entero.")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
    p = cursor.fetchone()
    conn.close()
    if p:
        print(f"{Fore.YELLOW}ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, "
              f"Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
    else:
        print(Fore.RED + "Producto no encontrado.")

def buscar_producto_por_nombre_o_categoria():
    """Busca productos por nombre o categoría y los muestra."""
    print(Fore.CYAN + "\n--- Buscar por nombre o categoría ---")
    texto = input("Ingrese texto para buscar: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE ? OR categoria LIKE ?",
        (f'%{texto}%', f'%{texto}%')
    )
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        for p in resultados:
            print(f"{Fore.YELLOW}ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, "
                  f"Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
    else:
        print(Fore.RED + "No se encontraron coincidencias.")

def actualizar_producto():
    """Actualiza los datos de un producto identificado por su ID."""
    print(Fore.CYAN + "\n--- Actualizar producto ---")
    id_prod = input("ID del producto a actualizar: ")
    if not id_prod.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    nombre = input("Nuevo nombre: ")
    descripcion = input("Nueva descripción: ")
    categoria = input("Nueva categoría: ")
    while True:
        try:
            cantidad = int(input("Nueva cantidad: "))
            break
        except ValueError:
            print(Fore.RED + "Cantidad debe ser número entero.")
    while True:
        try:
            precio = float(input("Nuevo precio: "))
            break
        except ValueError:
            print(Fore.RED + "Precio debe ser número válido.")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', (nombre, descripcion, cantidad, precio, categoria, id_prod))
    if cursor.rowcount == 0:
        print(Fore.RED + "No se encontró producto con ese ID.")
    else:
        print(Fore.GREEN + "Producto actualizado con éxito.")
    conn.commit()
    conn.close()

def eliminar_producto():
    """Elimina un producto de la base de datos por su ID."""
    print(Fore.CYAN + "\n--- Eliminar producto ---")
    id_prod = input("ID del producto a eliminar: ")
    if not id_prod.isdigit():
        print(Fore.RED + "ID inválido.")
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
    if cursor.rowcount == 0:
        print(Fore.RED + "No se encontró producto con ese ID.")
    else:
        print(Fore.GREEN + "Producto eliminado con éxito.")
    conn.commit()
    conn.close()

def reporte_baja_existencia():
    """Muestra productos con cantidad ≤ límite especificado por usuario."""
    print(Fore.CYAN + "\n--- Reporte de baja existencia ---")
    while True:
        try:
            limite = int(input("Mostrar productos con cantidad ≤: "))
            break
        except ValueError:
            print(Fore.RED + "Ingrese un número entero válido.")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    conn.close()
    if productos:
        print(Fore.YELLOW + f"\nProductos con cantidad ≤ {limite}:")
        for p in productos:
            print(f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[3]}, Categoría: {p[5]}")
    else:
        print(Fore.GREEN + "No hay productos con baja existencia.")

# -------------------- MENÚ PRINCIPAL --------------------

def mostrar_menu():
    """Muestra las opciones del menú principal."""
    print(Fore.BLUE + Style.BRIGHT + "\n========== MENÚ DE INVENTARIO ==========")
    print(Fore.WHITE + "1. Registrar producto")
    print("2. Ver todos los productos")
    print("3. Buscar producto por ID")
    print("4. Buscar por nombre o categoría")
    print("5. Actualizar producto")
    print("6. Eliminar producto")
    print("7. Reporte de baja existencia")
    print("0. Salir")

def menu():
    """Controla flujo del programa según opción elegida."""
    crear_tabla()
    while True:
        mostrar_menu()
        opcion = input(Fore.GREEN + "Seleccione una opción: ")
        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            ver_productos()
        elif opcion == '3':
            buscar_producto_por_id()
        elif opcion == '4':
            buscar_producto_por_nombre_o_categoria()
        elif opcion == '5':
            actualizar_producto()
        elif opcion == '6':
            eliminar_producto()
        elif opcion == '7':
            reporte_baja_existencia()
        elif opcion == '0':
            print(Fore.MAGENTA + "Gracias por usar el sistema de inventario 2025.")
            break
        else:
            print(Fore.RED + "Opción no válida, intente de nuevo.")

if __name__ == '__main__':
    menu()
