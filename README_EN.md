# Inventory Management System

## 📋 Description

The Inventory Management System is a simple application written in Python. It was developed as part of the Talento Tech course to practice programming concepts. The system allows managing products in a SQLite database.

---

## 🛠️ Features

- Add products to the inventory.
- View the full list of products.
- Update product information.
- Delete products from the inventory.
- Search for products using different parameters.
- Generate reports (low stock, by category).
- Reset the database.

---

## 🛑 Prerequisites

- Python 3.8 or higher.
- Required packages (see below).

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/FiodorPapor/inventory_manager.git
   cd inventory_manager
2. Set up a virtual environment (optional but recommended):
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python inventory_manager.py

## 📦 Dependencies

colorama: For colored terminal output.
Install all dependencies using:
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

MIT License.

## 👤 Author

Paporotskiy Fedor: Python student at Talento Tech.