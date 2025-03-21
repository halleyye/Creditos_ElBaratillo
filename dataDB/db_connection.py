# data/db_connection.py
import sqlite3
import os

DB_FILENAME = "creditos.db"

def get_db_connection():
    """
    Retorna una conexión a la base de datos SQLite.
    Si el archivo no existe, se creará automáticamente.
    """
    db_path = os.path.join(os.path.dirname(__file__), DB_FILENAME)
    connection = sqlite3.connect(db_path)
    # Para permitir columnas por nombre en el row_factory, si lo deseas:
    connection.row_factory = sqlite3.Row  
    return connection

def create_tables_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla Credits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Credits (
            CreditId INTEGER PRIMARY KEY AUTOINCREMENT,
            ClientName TEXT NOT NULL,
            Monto REAL NOT NULL,
            StartDate TEXT NOT NULL,
            DueDate TEXT NOT NULL,
            Status TEXT NOT NULL,
            Notes TEXT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
