# Inventory Management System

## 📋 Description

The Inventory Management System is a Python-based application developed during the Talento Tech course. It allows users to manage an inventory of products stored in a SQLite database. The system features a user-friendly terminal interface with colored output and formatted tables.

---

## 🛠️ Features

- **Product Management**:
  - Add products to the inventory.
  - View all products in a formatted table.
  - Update product details.
  - Delete products with confirmation prompts.
- **Search and Reporting**:
  - Search products by ID, name, category, and other parameters.
  - Generate reports for low stock or by category.
- **Database Management**:
  - Reset the database to start fresh.
- **Enhanced UI**:
  - Colored terminal output using `colorama`.
  - Table formatting with `tabulate`.

---

## 🛑 Prerequisites

- **Python**: Version 3.8 or higher.
- **Dependencies**: Listed in `requirements.txt`.

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FiodorPapor/inventory_manager.git
   cd inventory_manager
2. **Set up a virtual environment (optional but recommended)**:
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
3. **Install dependencies**:
   pip install -r requirements.txt
4. **Run the application**:
   python inventory_manager.py

## 📦 Dependencies

- **colorama**: For colored terminal output.
- **tabulate**: For formatted table output.

**Install all dependencies using**:
   pip install -r requirements.txt

## 📂 Project Structure

inventory_manager/
│
├── inventory_manager.py        # Main program file
├── inventario.db               # SQLite database file (auto-created)
├── requirements.txt            # List of dependencies
├── .gitignore                  # Git ignore rules
├── README_EN.md                # Documentation in English
└── README_ES.md                # Documentación en español

## 📖 License

This project is licensed under the MIT License.

## 👤 Author

Paporotskiy Fedor
Python student at Talento Tech.


