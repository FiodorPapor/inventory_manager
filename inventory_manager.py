import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama para salida de colores
init(autoreset=True)

# Conexión centralizada a la base de datos
def conectar_base_datos():
    try:
        return sqlite3.connect("inventario.db")
    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ Error al conectar con la base de datos: {e}")
        return None

# Inicialización de la base de datos si no existe
def inicializar_base_datos():
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()
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
    conexion.commit()
    conexion.close()
    print(Fore.GREEN + "✅ Base de datos inicializada correctamente.")

def agregar_producto():
    # Solicita los datos del usuario para el nuevo producto
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")

    while True:
        cantidad = input("Ingrese la cantidad del producto: ")
        if cantidad.isdigit() and int(cantidad) >= 0:
            cantidad = int(cantidad)
            break
        else:
            print("Por favor, ingrese una cantidad válida (número entero no negativo).")

    while True:
        precio = input("Ingrese el precio del producto: ")
        try:
            precio = float(precio)
            if precio >= 0:
                break
            else:
                print("El precio no puede ser negativo.")
        except ValueError:
            print("Por favor, ingrese un precio válido.")

    categoria = input("Ingrese la categoría del producto: ")

    # Conecta a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Pregunta al usuario si desea usar el último ID eliminado o continuar
    opcion = input("¿Desea continuar con el siguiente ID en la lista (ingrese '1') o desea usar el último ID eliminado (ingrese '2')? ")

    if opcion == '2':
        # Encuentra el siguiente ID disponible o usa el último ID eliminado
        cursor.execute("SELECT MIN(id + 1) FROM productos WHERE (id + 1) NOT IN (SELECT id FROM productos)")
        resultado = cursor.fetchone()
        if resultado[0] is not None:
            siguiente_id = resultado[0]
        else:
            # Si no hay IDs eliminados, obtiene el ID máximo o asigna 1 si la tabla está vacía
            max_id = cursor.execute("SELECT MAX(id) FROM productos").fetchone()[0]
            siguiente_id = max_id + 1 if max_id is not None else 1
    else:
        # Obtiene el próximo ID auto-incremental o asigna 1 si la tabla está vacía
        max_id = cursor.execute("SELECT MAX(id) FROM productos").fetchone()[0]
        siguiente_id = max_id + 1 if max_id is not None else 1

    # Inserta el producto con el ID determinado
    cursor.execute('''
        INSERT INTO productos (id, nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (siguiente_id, nombre, descripcion, cantidad, precio, categoria))

    # Guarda los cambios y cierra la conexión
    conexion.commit()
    conexion.close()

    print(f"¡Producto agregado exitosamente con ID: {siguiente_id}!")

def ver_productos():
    # Conecta a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Recibe todos los productos de la tabla 'productos'
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    # Verifica si hay productos en la base de datos
    if productos:
        print("Lista de productos en inventario:")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
    else:
        print("No hay productos en el inventario.")

    # Cierra la conexión a la base de datos
    conexion.close()


def actualizar_producto():
    # Conecta a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    while True:
        # Solicita el ID del producto a actualizar
        id_producto = input("Ingrese el ID del producto que desea actualizar (o 'salir' para cancelar): ")

        if id_producto.lower() == "salir":
            print("Operación cancelada.")
            conexion.close()
            return

        # Verifica si el ID ingresado es un número válido
        if not id_producto.isdigit():
            print("Por favor, ingrese un ID numérico válido.")
            continue

        id_producto = int(id_producto)

        # Verifica si el producto existe en la base de datos
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto is None:
            print("El producto con el ID proporcionado no existe. Inténtelo de nuevo.")
        else:
            break

    # Muestra los datos actuales y solicita nuevos valores
    print(f"Nombre actual: {producto[1]}")
    nuevo_nombre = input("Ingrese el nuevo nombre del producto (deje en blanco para mantener): ")
    if not nuevo_nombre:
        nuevo_nombre = producto[1]

    print(f"Descripción actual: {producto[2]}")
    nueva_descripcion = input("Ingrese la nueva descripción del producto (deje en blanco para mantener): ")
    if not nueva_descripcion:
        nueva_descripcion = producto[2]

    while True:
        print(f"Cantidad actual: {producto[3]}")
        nueva_cantidad = input("Ingrese la nueva cantidad del producto (deje en blanco para mantener): ")
        if not nueva_cantidad:
            nueva_cantidad = producto[3]
            break
        elif nueva_cantidad.isdigit() and int(nueva_cantidad) >= 0:
            nueva_cantidad = int(nueva_cantidad)
            break
        else:
            print("Por favor, ingrese una cantidad válida.")

    while True:
        print(f"Precio actual: {producto[4]}")
        nuevo_precio = input("Ingrese el nuevo precio del producto (deje en blanco para mantener): ")
        if not nuevo_precio:
            nuevo_precio = producto[4]
            break
        try:
            nuevo_precio = float(nuevo_precio)
            if nuevo_precio >= 0:
                break
            else:
                print("El precio no puede ser negativo.")
        except ValueError:
            print("Por favor, ingrese un precio válido.")

    print(f"Categoría actual: {producto[5]}")
    nueva_categoria = input("Ingrese la nueva categoría del producto (deje en blanco para mantener): ")
    if not nueva_categoria:
        nueva_categoria = producto[5]

    # Actualiza los datos del producto en la base de datos
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))

    # Guarda los cambios y cierra la conexión
    conexion.commit()
    conexion.close()

    print("¡Producto actualizado exitosamente!")

def eliminar_producto():
    # Conecta a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    while True:
        # Solicita el ID del producto a eliminar
        id_producto = input("Ingrese el ID del producto que desea eliminar (o 'salir' para cancelar): ")

        if id_producto.lower() == "salir":
            print("Operación cancelada.")
            conexion.close()
            return

        # Verifica si el ID ingresado es un número válido
        if not id_producto.isdigit():
            print("Por favor, ingrese un ID numérico válido.")
            continue

        id_producto = int(id_producto)

        # Verifica si el producto existe en la base de datos
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto is None:
            print("El producto con el ID proporcionado no existe. Inténtelo de nuevo.")
        else:
            # Elimina el producto de la tabla 'productos'
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            print("¡Producto eliminado exitosamente!")
            break

    # Guarda los cambios y cierra la conexión
    conexion.commit()
    conexion.close()

def buscar_producto():
    # Conexión a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Menú para seleccionar el criterio de búsqueda
    print("\n🔍 BUSCAR PRODUCTO POR PARÁMETROS")
    print("Opciones de búsqueda:")
    print("1. ID")
    print("2. Nombre")
    print("3. Descripción")
    print("4. Cantidad")
    print("5. Precio")
    print("6. Categoría")
    print("7. Volver al menú principal")

    opcion = input("Seleccione una opción (1-7): ")

    if opcion == "7":
        # Cerrar la conexión y regresar al menú
        print("Volviendo al menú principal...")
        conexion.close()
        return

    # Definir los campos disponibles para buscar
    campos = {
        "1": "id",
        "2": "nombre",
        "3": "descripcion",
        "4": "cantidad",
        "5": "precio",
        "6": "categoria"
    }

    # Obtener el campo según la opción seleccionada
    campo = campos.get(opcion)

    if not campo:
        print("⚠️ Opción no válida. Intente de nuevo.")
    else:
        # Solicitar el valor para buscar
        valor = input(f"Ingrese el valor para buscar en '{campo}': ")

        # Construir la consulta SQL según el tipo de campo
        if campo in ["nombre", "descripcion", "categoria"]:
            # Para texto, buscar coincidencias parciales usando LIKE
            cursor.execute(f"SELECT * FROM productos WHERE {campo} LIKE ?", (f"%{valor}%",))
        else:
            # Para números, buscar coincidencias exactas
            cursor.execute(f"SELECT * FROM productos WHERE {campo} = ?", (valor,))

        # Obtener y mostrar los resultados
        productos = cursor.fetchall()

        if productos:
            print("\nProductos encontrados:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
        else:
            print("⚠️ No se encontraron productos que coincidan con el criterio de búsqueda.")

    # Cerrar la conexión a la base de datos
    conexion.close()

def generar_reportes():
    # Conexión a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    print("\n📊 GENERAR REPORTES")
    print("1. Productos con bajo stock")
    print("2. Productos por categoría")
    print("3. Volver al menú principal")

    opcion = input("Seleccione una opción (1-3): ")

    if opcion == "1":
        # Reporte de productos con bajo stock
        try:
            limite = int(input("Ingrese el límite de stock para el reporte: "))
            cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
            productos = cursor.fetchall()

            if productos:
                print("\nProductos con bajo stock:")
                for producto in productos:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
            else:
                print("⚠️ No hay productos con stock bajo según el límite proporcionado.")
        except ValueError:
            print("⚠️ Por favor, ingrese un número válido para el límite de stock.")

    elif opcion == "2":
        # Reporte de productos por categoría
        categoria = input("Ingrese la categoría para generar el reporte: ")
        cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
        productos = cursor.fetchall()

        if productos:
            print(f"\nProductos en la categoría '{categoria}':")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
        else:
            print(f"⚠️ No se encontraron productos en la categoría '{categoria}'.")

    elif opcion == "3":
        print("Volviendo al menú principal...")
    else:
        print("⚠️ Opción no válida. Intente de nuevo.")

    # Cierra la conexión a la base de datos
    conexion.close()

def resetear_base_datos():
    # Primer advertencia al usuario
    confirmacion = input("⚠️ ATENCIÓN: Esta acción eliminará TODOS los productos de la base de datos de forma permanente. ¿Desea continuar? (y/n): ")
    if confirmacion.lower() != "y":
        print("Operación cancelada.")
        return

    # Segunda advertencia para confirmar
    confirmacion_final = input("⚠️ CONFIRMACIÓN FINAL: Está a punto de eliminar todos los datos de la base. Escriba 'y' para confirmar: ")
    if confirmacion_final != "y":
        print("Operación cancelada.")
        return

    # Conecta a la base de datos y elimina todos los productos, reseteando el ID
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    # Elimina todos los registros de la tabla 'productos' y reinicia el ID auto-incremental
    cursor.execute("DELETE FROM productos")  # Elimina todas las filas en la tabla 'productos'
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos'")  # Reinicia el contador de ID

    # Guarda los cambios y cierra la conexión a la base de datos
    conexion.commit()
    conexion.close()
    print("✅ Todos los productos han sido eliminados y el ID fue reseteado.")

def menu_principal():
    while True:
        # Encabezado del menú
        print(Fore.CYAN + "\n📋 MENÚ PRINCIPAL")
        print(Fore.GREEN + "1. Agregar producto")
        print(Fore.GREEN + "2. Ver productos")
        print(Fore.GREEN + "3. Actualizar producto")
        print(Fore.GREEN + "4. Eliminar producto")
        print(Fore.GREEN + "5. Buscar producto")
        print(Fore.GREEN + "6. Generar reportes")
        print(Fore.GREEN + "7. Resetear base de datos")
        print(Fore.RED + "8. Salir")

        # Solicitar opción del usuario
        opcion = input(Fore.YELLOW + "Seleccione una opción (1-8): ")

        # Procesar opción seleccionada
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            generar_reportes()
        elif opcion == "7":
            resetear_base_datos()
        elif opcion == "8":
            print(Fore.BLUE + "¡Gracias por usar el sistema de inventario!")
            break
        else:
            print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    conectar_base_datos()
    inicializar_base_datos()
    menu_principal()