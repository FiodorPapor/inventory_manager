import sqlite3
from colorama import Fore, Style, init
from tabulate import tabulate

# Inicializar colorama para salida de colores
init(autoreset=True)

# Conexión centralizada a la base de datos
def conectar_base_datos():
    """
    Conecta a la base de datos SQLite. Si ocurre un error, lo maneja.
    """
    try:
        return sqlite3.connect("inventario.db")
    except sqlite3.Error as e:
        print(Fore.RED + f"⚠️ Error al conectar con la base de datos: {e}")
        return None

# Inicialización de la base de datos si no existe
def inicializar_base_datos():
    """
    Crea la tabla 'productos' si no existe en la base de datos.
    """
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

# Función para agregar un producto al inventario
def agregar_producto():
    """
    Solicita al usuario datos del producto y los guarda en la base de datos.
    Permite al usuario elegir entre continuar con ID automático o usar el último ID eliminado.
    """
    print(Fore.CYAN + "\n📝 Agregar Producto")
    
    # Solicita el nombre del producto
    nombre = input("Ingrese el nombre del producto: ")

    # Validar que el nombre no sea vacío ni contenga solo espacios
    while not nombre.strip():
        print(Fore.RED + "⚠️ El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre del producto: ")

    descripcion = input("Ingrese la descripción del producto: ")

    # Solicita la categoría del producto
    categoria = input("Ingrese la categoría del producto: ")

    # Validar que la categoría no sea vacía ni contenga solo espacios
    while not categoria.strip():
        print(Fore.RED + "⚠️ La categoría no puede estar vacía.")
        categoria = input("Ingrese la categoría del producto: ")

    # Validación de cantidad
    while True:
        cantidad = input("Ingrese la cantidad del producto: ")
        if cantidad.isdigit() and int(cantidad) >= 0:
            cantidad = int(cantidad)
            break
        else:
            print(Fore.RED + "⚠️ Por favor, ingrese una cantidad válida (número entero no negativo).")

    # Validación de precio
    while True:
        precio = input("Ingrese el precio del producto: ")
        try:
            precio = float(precio)
            if precio >= 0:
                break
            else:
                print(Fore.RED + "⚠️ El precio no puede ser negativo.")
        except ValueError:
            print(Fore.RED + "⚠️ Por favor, ingrese un precio válido.")

    # Conexión a la base de datos
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Elección del método de asignación del ID
    # La lógica de elección de ID permite reutilizar valores liberados, minimizando 
    # las brechas en la secuencia de IDs. Esto es útil si el ID tiene relevancia 
    # fuera de la base de datos, como en reportes o referencias externas.

    opcion = input("¿Desea continuar con el siguiente ID en la lista (ingrese '1') o usar el último ID eliminado (ingrese '2')? ")

    if opcion == '2':
        # Recuperar el primer ID disponible que no está en uso
        cursor.execute("""
            SELECT MIN(posible_id)
            FROM (
                SELECT id + 1 AS posible_id
                FROM productos
                EXCEPT
                SELECT id FROM productos
            )
            WHERE posible_id IS NOT NULL
        """)
        resultado = cursor.fetchone()
        siguiente_id = resultado[0] if resultado and resultado[0] else None

        # Si no hay IDs libres, usar el próximo ID secuencial
        if siguiente_id is None:
            cursor.execute("SELECT MAX(id) FROM productos")
            max_id = cursor.fetchone()[0]
            siguiente_id = max_id + 1 if max_id else 1
    else:
        # Usar el próximo ID automático
        cursor.execute("SELECT MAX(id) FROM productos")
        max_id = cursor.fetchone()[0]
        siguiente_id = max_id + 1 if max_id else 1

    # Insertar el producto con el ID seleccionado
    cursor.execute('''
        INSERT INTO productos (id, nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (siguiente_id, nombre, descripcion, cantidad, precio, categoria))

    # Confirmar y cerrar conexión
    conexion.commit()
    conexion.close()

    print(Fore.GREEN + f"✅ Producto agregado exitosamente con ID: {siguiente_id}")

# Función para ver todos los productos
def ver_productos():
    """
    Muestra todos los productos en la base de datos.
    """
    print(Fore.CYAN + "\n📦 Ver Productos")
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if productos:
        print(Fore.GREEN + "Lista de productos en inventario:")
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
    else:
        print(Fore.RED + "⚠️ No hay productos en el inventario.")

    conexion.close()

# Función para actualizar un producto existente
def actualizar_producto():
    """
    Permite al usuario actualizar los datos de un producto específico.
    Solicita el ID del producto y ofrece opciones para modificar cada campo.
    """
    print(Fore.CYAN + "\n✏️ Actualizar Producto")
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    while True:
        # Solicita el ID del producto a actualizar
        id_producto = input("Ingrese el ID del producto que desea actualizar (o 'salir' para cancelar): ")

        if id_producto.lower() == "salir":
            print(Fore.YELLOW + "Operación cancelada.")
            conexion.close()
            return

        # Verifica si el ID ingresado es un número válido
        if not id_producto.isdigit():
            print(Fore.RED + "⚠️ Por favor, ingrese un ID numérico válido.")
            continue

        id_producto = int(id_producto)

        # Verifica si el producto existe en la base de datos
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto is None:
            print(Fore.RED + "⚠️ El producto con el ID proporcionado no existe. Inténtelo de nuevo.")
        else:
            break

    # Muestra los datos actuales y solicita nuevos valores
    print(Fore.YELLOW + f"Nombre actual: {producto[1]}")
    nuevo_nombre = input("Ingrese el nuevo nombre del producto (deje en blanco para mantener): ") or producto[1]

    print(Fore.YELLOW + f"Descripción actual: {producto[2]}")
    nueva_descripcion = input("Ingrese la nueva descripción del producto (deje en blanco para mantener): ") or producto[2]

    while True:
        print(Fore.YELLOW + f"Cantidad actual: {producto[3]}")
        nueva_cantidad = input("Ingrese la nueva cantidad del producto (deje en blanco para mantener): ")
        if not nueva_cantidad:
            nueva_cantidad = producto[3]
            break
        elif nueva_cantidad.isdigit() and int(nueva_cantidad) >= 0:
            nueva_cantidad = int(nueva_cantidad)
            break
        else:
            print(Fore.RED + "⚠️ Por favor, ingrese una cantidad válida.")

    while True:
        print(Fore.YELLOW + f"Precio actual: {producto[4]}")
        nuevo_precio = input("Ingrese el nuevo precio del producto (deje en blanco para mantener): ")
        if not nuevo_precio:
            nuevo_precio = producto[4]
            break
        try:
            nuevo_precio = float(nuevo_precio)
            if nuevo_precio >= 0:
                break
            else:
                print(Fore.RED + "⚠️ El precio no puede ser negativo.")
        except ValueError:
            print(Fore.RED + "⚠️ Por favor, ingrese un precio válido.")

    print(Fore.YELLOW + f"Categoría actual: {producto[5]}")
    nueva_categoria = input("Ingrese la nueva categoría del producto (deje en blanco para mantener): ") or producto[5]

    # Actualiza los datos del producto en la base de datos
    cursor.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    ''', (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))

    # Guarda los cambios y cierra la conexión
    conexion.commit()
    conexion.close()

    print(Fore.GREEN + "✅ ¡Producto actualizado exitosamente!")

# Función para eliminar un producto
def eliminar_producto():
    """
    Permite eliminar un producto por su ID.
    Solicita confirmación antes de realizar la eliminación.
    """
    print(Fore.CYAN + "\n❌ Eliminar Producto")
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    while True:
        # Solicita el ID del producto a eliminar
        id_producto = input("Ingrese el ID del producto que desea eliminar (o 'salir' para cancelar): ")

        if id_producto.lower() == "salir":
            print(Fore.YELLOW + "Operación cancelada.")
            conexion.close()
            return

        # Verifica si el ID ingresado es un número válido
        if not id_producto.isdigit():
            print(Fore.RED + "⚠️ Por favor, ingrese un ID numérico válido.")
            continue

        id_producto = int(id_producto)

        # Verifica si el producto existe en la base de datos
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if producto is None:
            print(Fore.RED + "⚠️ El producto con el ID proporcionado no existe. Inténtelo de nuevo.")
        else:
            # Solicita confirmación antes de eliminar
            confirmacion = input(Fore.RED + f"⚠️ ¿Está seguro de que desea eliminar el producto '{producto[1]}'? (y/n): ")
            if confirmacion.lower() == 'y':
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                print(Fore.GREEN + "✅ ¡Producto eliminado exitosamente!")
                break
            else:
                print(Fore.YELLOW + "Operación cancelada.")
                break

    # Guarda los cambios y cierra la conexión
    conexion.commit()
    conexion.close()

# Función para buscar productos por criterios
def buscar_producto():
    """
    Permite buscar productos en la base de datos según varios criterios.
    """
    print(Fore.CYAN + "\n🔍 Buscar Producto")
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Menú para seleccionar el criterio de búsqueda
    print(Fore.YELLOW + "Opciones de búsqueda:")
    print("1. ID")
    print("2. Nombre")
    print("3. Descripción")
    print("4. Cantidad")
    print("5. Precio")
    print("6. Categoría")
    print("7. Volver al menú principal")

    opcion = input("Seleccione una opción (1-7): ")

    if opcion == "7":
        print(Fore.YELLOW + "Volviendo al menú principal...")
        conexion.close()
        return

    # Mapa de opciones a campos de la base de datos
    campos = {
        "1": "id",
        "2": "nombre",
        "3": "descripcion",
        "4": "cantidad",
        "5": "precio",
        "6": "categoria"
    }

    # Obtener el campo seleccionado
    campo = campos.get(opcion)

    # Verifica si el campo seleccionado es válido
    if not campo:
        print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")
    else:
        # Solicita el valor para buscar
        valor = input(f"Ingrese el valor para buscar en '{campo}': ")

        # Validar que el valor ingresado no sea vacío
        while not valor.strip():
            print(Fore.RED + "⚠️ El valor no puede estar vacío.")
            valor = input(f"Ingrese el valor para buscar en '{campo}': ")

        # Determina el tipo de búsqueda según el campo
        if campo in ["nombre", "descripcion", "categoria"]:
            cursor.execute(f"SELECT * FROM productos WHERE {campo} LIKE ?", (f"%{valor}%",))
        else:
            cursor.execute(f"SELECT * FROM productos WHERE {campo} = ?", (valor,))

        # Obtener los resultados de la búsqueda
        productos = cursor.fetchall()

        if productos:
            print(Fore.GREEN + "\nProductos encontrados:")
            headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
            print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
        else:
            print(Fore.RED + "⚠️ No se encontraron productos que coincidan con el criterio de búsqueda.")

    # Cerrar la conexión a la base de datos
    conexion.close()

# Función para generar reportes del inventario
def generar_reportes():
    """
    Permite generar reportes según criterios específicos:
    - Productos con bajo stock.
    - Productos agrupados por categoría.
    """
    print(Fore.CYAN + "\n📊 Generar Reportes")
    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    print(Fore.YELLOW + "Opciones de reporte:")
    print("1. Productos con bajo stock")
    print("2. Productos por categoría")
    print("3. Volver al menú principal")

    opcion = input("Seleccione una opción (1-3): ")

    try:
        if opcion == "1":
            # Reporte de productos con bajo stock
            try:
                limite = int(input("Ingrese el límite de stock para el reporte: "))
                cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
                productos = cursor.fetchall()

                if productos:
                    print(Fore.GREEN + "\nProductos con bajo stock:")
                    headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
                    print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
                else:
                    print(Fore.RED + "⚠️ No hay productos con stock bajo según el límite proporcionado.")
            except ValueError:
                print(Fore.RED + "⚠️ Por favor, ingrese un número válido para el límite de stock.")

        elif opcion == "2":
            # Reporte de productos por categoría
            categoria = input("Ingrese la categoría para generar el reporte: ")
            cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
            productos = cursor.fetchall()

            if productos:
                print(Fore.GREEN + f"\nProductos en la categoría '{categoria}':")
                headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
                print(tabulate(productos, headers=headers, tablefmt="fancy_grid"))
            else:
                print(Fore.RED + f"⚠️ No se encontraron productos en la categoría '{categoria}'.")

        elif opcion == "3":
            print(Fore.YELLOW + "Volviendo al menú principal...")
        else:
            print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")

    finally:
        # Cerrar la conexión a la base de datos
        conexion.close()

# Función para resetear la base de datos
def resetear_base_datos():
    """
    Elimina todos los productos en la base de datos y reinicia el contador de IDs.
    Solicita confirmaciones múltiples para evitar errores accidentales.
    """
    print(Fore.RED + "\n⚠️ ATENCIÓN: Esta acción eliminará TODOS los productos de la base de datos de forma permanente.")
    confirmacion = input("¿Está seguro de que desea continuar? Escriba 'y' para confirmar, 'n' para cancelar: ")

    if confirmacion.lower() != 'y':
        print(Fore.YELLOW + "Operación cancelada.")
        return

    confirmacion_final = input(Fore.RED + "CONFIRMACIÓN FINAL: Escriba 'eliminar todo' para proceder: ")

    if confirmacion_final.lower() != "eliminar todo":
        print(Fore.YELLOW + "Operación cancelada.")
        return

    conexion = conectar_base_datos()
    if conexion is None:
        return

    cursor = conexion.cursor()

    # Elimina todos los registros de la tabla y reinicia el ID auto-incremental
    cursor.execute("DELETE FROM productos")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos'")

    conexion.commit()
    conexion.close()

    print(Fore.GREEN + "✅ Todos los productos han sido eliminados y el ID fue reseteado.")

def menu_productos():
    """
    Submenú para la gestión de productos en el inventario.
    Permite agregar, ver, actualizar y eliminar productos.
    """
    while True:
        print(Fore.CYAN + "\n📋 MENÚ GESTIÓN DE PRODUCTOS")
        print(Fore.GREEN + "1. Agregar producto")
        print(Fore.GREEN + "2. Ver productos")
        print(Fore.GREEN + "3. Actualizar producto")
        print(Fore.GREEN + "4. Eliminar producto")
        print(Fore.YELLOW + "5. Volver al menú principal")

        opcion = input(Fore.YELLOW + "Seleccione una opción (1-5): ")

        if opcion == "1":
            agregar_producto()  # Llama a la función para agregar un producto
        elif opcion == "2":
            ver_productos()  # Llama a la función para visualizar productos
        elif opcion == "3":
            actualizar_producto()  # Llama a la función para actualizar un producto
        elif opcion == "4":
            eliminar_producto()  # Llama a la función para eliminar un producto
        elif opcion == "5":
            break  # Vuelve al menú principal
        else:
            print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")

def menu_reportes():
    """
    Submenú para reportes y búsqueda.
    Incluye opciones para buscar productos, generar reportes y resetear la base de datos.
    """
    while True:
        print(Fore.CYAN + "\n📋 MENÚ REPORTES Y BÚSQUEDA")
        print(Fore.GREEN + "1. Buscar producto")
        print(Fore.GREEN + "2. Generar reportes")
        print(Fore.RED + "3. Resetear base de datos")
        print(Fore.YELLOW + "4. Volver al menú principal")

        opcion = input(Fore.YELLOW + "Seleccione una opción (1-4): ")

        if opcion == "1":
            buscar_producto()  # Llama a la función para buscar productos en la base
        elif opcion == "2":
            generar_reportes()  # Llama a la función para generar reportes
        elif opcion == "3":
            resetear_base_datos()  # Llama a la función para resetear la base de datos
        elif opcion == "4":
            break  # Vuelve al menú principal
        else:
            print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")

# Menú principal del sistema
def menu_principal():
    """
    Muestra el menú principal del sistema.
    Divide las operaciones en dos grupos: gestión de productos y reportes.
    """
    while True:
        print(Fore.CYAN + "\n📋 MENÚ PRINCIPAL")
        print(Fore.GREEN + "1. Gestión de productos")
        print(Fore.GREEN + "2. Reportes y búsqueda")
        print(Fore.RED + "3. Salir")

        # Solicita al usuario que elija una opción
        opcion = input(Fore.YELLOW + "Seleccione una opción (1-3): ")

        if opcion == "1":
            menu_productos()  # Accede al submenú para gestionar productos
        elif opcion == "2":
            menu_reportes()  # Accede al submenú para reportes y búsqueda
        elif opcion == "3":
            print(Fore.BLUE + "¡Gracias por usar el sistema de inventario!")
            break
        else:
            print(Fore.RED + "⚠️ Opción no válida. Intente de nuevo.")

# Función principal para ejecutar el programa
def main():
    """
    Función principal que inicializa la base de datos y muestra el menú principal.
    """
    inicializar_base_datos()
    menu_principal()

# Ejecutar el programa
if __name__ == "__main__":
    """
    Este bloque garantiza que el programa se ejecuta solo si es el archivo principal.
    """
    main()

# Fin del programa