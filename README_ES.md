# Sistema de Gestión de Inventario

## 📋 Descripción

El Sistema de Gestión de Inventario es una aplicación sencilla escrita en Python. Fue desarrollada como parte del curso de Talento Tech para practicar conceptos de programación. El sistema permite gestionar productos en una base de datos SQLite.

---

## 🛠️ Funcionalidades

- Agregar productos al inventario.
- Ver la lista completa de productos.
- Actualizar información de productos.
- Eliminar productos del inventario.
- Buscar productos por diferentes parámetros.
- Generar reportes (productos con bajo stock, por categoría).
- Resetear la base de datos.

---

## 🛑 Requisitos

- Python 3.8 o superior.
- Paquetes requeridos (ver más abajo).

---

## 🚀 Cómo ejecutar

1. Clona este repositorio:
   ```bash
   git clone https://github.com/FiodorPapor/inventory_manager.git
   cd inventory_manager
2. Configura un entorno virtual (opcional pero recomendado):
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
3. Instala las dependencias:
   pip install -r requirements.txt
4. Ejecuta la aplicación:
   python inventory_manager.py

## 📦 Dependencias

- colorama: Para colores en la salida del terminal.
Instala todas las dependencias usando:
   pip install -r requirements.txt

## 📂 Estructura del Proyecto

inventory_manager/
│
├── inventory_manager.py        # Archivo principal del programa
├── inventario.db               # Archivo de base de datos SQLite (creado automáticamente)
├── requirements.txt            # Lista de dependencias
├── .gitignore                  # Reglas para ignorar archivos innecesarios
├── README_EN.md                # Documentation in English
└── README_ES.md                # Documentación en español

## 📖 License

MIT License.

## 👤 Autor

Paporotskiy Fedor: Estudiante de programación en Talento Tech.