# Sistema de Gestión de Inventario

## 📋 Descripción

El Sistema de Gestión de Inventario es una aplicación desarrollada en Python durante el curso de Talento Tech. Permite gestionar productos almacenados en una base de datos SQLite con una interfaz amigable basada en la terminal. 

---

## 🛠️ Funcionalidades

- **Gestión de Productos**:
  - Agregar productos al inventario.
  - Ver todos los productos en una tabla formateada.
  - Actualizar información de productos.
  - Eliminar productos con confirmación.
- **Búsqueda y Reportes**:
  - Buscar productos por ID, nombre, categoría y otros parámetros.
  - Generar reportes de productos con bajo stock o por categoría.
- **Gestión de la Base de Datos**:
  - Resetear la base de datos para empezar desde cero.
- **Interfaz Mejorada**:
  - Salida de terminal en colores usando `colorama`.
  - Tablas formateadas con `tabulate`.

---

## 🛑 Requisitos

- **Python**: Versión 3.8 o superior.
- **Dependencias**: Listadas en `requirements.txt`.

---

## 🚀 Cómo ejecutar

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/FiodorPapor/inventory_manager.git
   cd inventory_manager
2. **Configura un entorno virtual (opcional pero recomendado)**:
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
3. **Instala las dependencias**:
   pip install -r requirements.txt
4. **Ejecuta la aplicación**:
   python inventory_manager.py

## 📦 Dependencias

- **colorama**: Para colores en la salida del terminal.
- **tabulate**: Para tablas con formato.

**Instala todas las dependencias con**:
   pip install -r requirements.txt

## 📂 Estructura del Proyecto

inventory_manager/
│
├── inventory_manager.py        # Archivo principal del programa
├── inventario.db               # Archivo de base de datos SQLite (creado automáticamente)
├── requirements.txt            # Lista de dependencias
├── .gitignore                  # Reglas para ignorar archivos innecesarios
├── README_EN.md                # Documentación en inglés
└── README_ES.md                # Documentación en español

## 📖 Licencia
Este proyecto está licenciado bajo la Licencia MIT.

## 👤 Autor
Paporotskiy Fedor
Estudiante de programación en Talento Tech.

